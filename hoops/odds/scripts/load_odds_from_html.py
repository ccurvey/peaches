import os.path
from datetime import date

from bs4 import BeautifulSoup

import django
django.setup()

from games.models import School, Game, Team, Season, SchoolAlias
from odds.models import GameMoney, GameSide, GameTotal

ALL_SCHOOLS = [s.name for s in School.objects.all()]
missing_schools = set()

"""
This is what the data looks like for a game in April 2008
Date    Roto   Location School        1st     2nd     Final   Open    Close   ML     2nd
401	667	N	Massachusetts	27	51	78	153	156	170	0.5
401	668	N	Florida      	36	30	66	3	4	-200	82

So what we should get out of there is

1) UMass +4 (game)
2) Umass -0.5 (2nd half)
3) Florida -4 (game)
4) Florida +0.5 (2nd half)
5) Over 156 (game)
6) Under 156 (game)
7) Over 82 (2nd half)
8) Under 82 (2nd half)
9) Umass ML (+170)
10) Florida ML (-200)

(bets 1-8 are all -110)

So we will have two "game" records

ID      Team       Opponent
1       UMass      Fla
2       Fla        Umass

and we want the following bet records
ID    GameID    LineType      LineValue      Odds
1     1         GS            +4             -110
2     1         2S            -0.5           -110
3     2         GS            -4             -110
4     2         2S            +0.5           -110
5     1         GT            156            -110 # dup?
6     2         GT            156            -110 # dup?
7     1         2T            82             -110 # dup?
8     2         2T            82             -110 # dup?
9     1         ML            0              +170
10    2         ML            0              -200

No, wait.  There's two kinds of bets here:  side and total

Side Bets:
Umass +4    -110 (game)
Umass +0    +170 (game)
Umass -0.5  -110 (2nd)

Fla   -4    -110 (game)
Fla   +0    -200 (game)
Fla   +0.5   -110 (2nd)

Over 156    -110 (game)
Under 156   -110 (game)

Over 82     -110 (2nd)
Under 82    -110 (2nd)
"""

class Line(object):
    def __init__(self, cells, year):
        mmdd = ('0' + cells[0].get_text())[-4:]
        try:
            self.game_date = date(year, int(mmdd[:2]), int(mmdd[2:]))
        except ValueError:
            pass

        self.roto = cells[1].get_text()
        self.location = cells[2].get_text().strip()
        self.school_name = cells[3].get_text().strip()
        self.school_name = "".join([i for i in self.school_name if 31 < ord(i) < 127])
        self.first_half_score = cells[4].get_text()
        self.second_half_score = cells[5].get_text()
        self.final_score = cells[6].get_text().strip()
        open_prop = cells[7].get_text() # could be spread or total
        self.close = cells[8].get_text() # could be spread or total
        if self.close == 'pk':
            self.close = 0
        elif self.close == "NL":
            self.close = None
        else:
            self.close = float(self.close)

        money_line = cells[9].get_text()
        if money_line == 'NL':
            self.money_line = None
        else:
            self.money_line = money_line

        self.second_half_prop = cells[10].get_text()
        if self.second_half_prop == 'pk':
            self.second_half_prop = 0
        elif self.second_half_prop == "NL":
            self.second_half_prop = None
        else:
            self.second_half_prop = float(self.second_half_prop)

    def get_school(self):
        try:
            return School.objects.get(name__iexact=self.name)
        except School.DoesNotExist, e:
            try:
                alias = SchoolAlias.objects.get(alias__iexact=self.name)
                return alias.school
            except SchoolAlias.DoesNotExist:
                missing_schools.add(self.name)
                (best_name, match_score) = process.extractOne(self.name, ALL_SCHOOLS)
                if best_name:
                    try:
                        return School.objects.get(name=best_name)
                    except School.DoesNotExist:
                        raise
            raise e
    school = property(get_school)

    def get_team(self):
        season = Season.objects.get(start_date__lte = self.game_date,
                                    end_date__gte = self.game_date)

        return Team.objects.get(school=self.school, season=season)
    team = property(get_team)

############################################################################
class PropGenerator(object):
    def __init__(self, year):
        self.line_pair = []
        self.year = year
        self._by_school = dict()

    def add_line(self, line):
        self.line_pair.append(line)
        #if len(self.line_pair) == 2:
            #dog_line = BettingLine(self.dog_spread, self.dog_money_line,
                                   #self.total)
            #self._by_school[self.dog_school] = dog_line

            #favorite_line = BettingLine(self.favorite_spread,
                                        #self.favorite_money_line,
                                        #self.total)
            #self._by_school[self.favorite_school] = favorite_line
            #self._by_school[self.dog_school] = dog_line

    def get_favorite_line(self):
        if self.line_pair[0].close < self.line_pair[1].close:
            return self.line_pair[0]
        elif self.line_pair[0].close == self.line_pair[1].close:
            return self.line_pair[0]
        return self.line_pair[1]
    favorite_line = property(get_favorite_line)

    def get_favorite_school(self):
        return self.favorite_line.school_name
    favorite_school = property(get_favorite_school)

    def get_favorite_spread(self):
        try:
            return self.favorite_line.close * -1
        except TypeError:
            return None
    favorite_spread = property(get_favorite_spread)

    def get_favorite_money_line(self):
        return self.favorite_line.money_line
    favorite_money_line = property(get_favorite_money_line)

    def get_dog_line(self):
        if self.line_pair[0].close > self.line_pair[1].close:
            return self.line_pair[0]
        return self.line_pair[1]
    dog_line = property(get_dog_line)

    def get_dog_school(self):
        return self.dog_line.school_name
    dog_school = property(get_dog_school)

    def get_dog_spread(self):
        try:
            return self.favorite_spread * -1
        except TypeError:
            return None
    dog_spread = property(get_dog_spread)

    def get_dog_money_line(self):
        return self.dog_line.money_line
    dog_money_line = property(get_dog_money_line)

    def get_total(self):
        return self.dog_line.close
    total = property(get_total)

    def get_game_date(self):
        return self.line_pair[0].game_date
    game_date = property(get_game_date)

    def get_school_line(self, school_name):
        return self._by_school[school_name]

    def generate_props(self):
        # now we have to find the school/team/game
        try:
            fav_school = SchoolAlias.objects.get(alias=self.favorite_school).school
        except SchoolAlias.DoesNotExist:
            if not self.favorite_school in missing_schools:
                print "could not find %s" % self.favorite_school
                missing_schools.add(self.favorite_school)
            fav_school = None

        try:
            dog_school = SchoolAlias.objects.get(alias=self.dog_school).school
        except SchoolAlias.DoesNotExist:
            if not self.dog_school in missing_schools:
                print "could not find %s" % self.dog_school
                missing_schools.add(self.dog_school)
            dog_school = None

        try:
            season = Season.objects.get(start_date__lte=self.game_date,
                                        end_date__gte=self.game_date)
        except Season.DoesNotExist:
            print "could not find season for date %s" % self.game_date
            season = None

        if all((season, fav_school, dog_school)):
            fav_team, created = Team.objects.get_or_create(school=fav_school,
                                                           season=season)
            dog_team, created = Team.objects.get_or_create(school=dog_school,
                                                           season=season)

            try:
                fav_game = Game.objects.get(game_date=self.game_date,
                                        team=fav_team, opponent=dog_team)
            except Game.DoesNotExist:
                print "could not find game for %s vs %s on %s" % (
                    fav_team.school.name, dog_team.school.name,
                    self.game_date)
            else:
                if self.favorite_spread is not None:
                    GameSide.objects.get_or_create(game=fav_game,
                                                   class_name="GameSide",
                                                   defaults={"value" : self.favorite_spread})
                if self.favorite_money_line is not None:
                    GameMoney.objects.get_or_create(game=fav_game,
                                                    class_name="GameMoney",
                                                    defaults={"payoff" : self.favorite_money_line})
                if self.total is not None:
                    GameTotal.objects.get_or_create(game=fav_game,
                                                    class_name="GameTotal",
                                                    defaults={"value" : self.total})

            try:
                dog_game = Game.objects.get(game_date=self.game_date,
                                        team=dog_team, opponent=fav_team)
            except Game.DoesNotExist:
                print "could not find game for %s vs %s on %s" % (
                    dog_team.school.name, fav_team.school.name,
                    self.game_date)
            else:
                if self.dog_spread is not None:
                    GameSide.objects.get_or_create(game=dog_game,
                                                   class_name="GameSide",
                                                   defaults={"value" : self.dog_spread})
                if self.dog_money_line is not None:
                    GameMoney.objects.get_or_create(game=dog_game,
                                                    class_name="GameMoney",
                                                    defaults={"payoff" : self.dog_money_line})
                if self.total is not None:
                    GameTotal.objects.get_or_create(game=dog_game,
                                                    class_name="GameTotal",
                                                    defaults={"value" : self.total})



############################################################################
from odds.models import GameMoney, GameSide, GameTotal
def process_file(filename):
    soup = BeautifulSoup(open(filename, "r"))

    (f, ext) = os.path.splitext(filename)
    year = int(f[-4:])
    pg = PropGenerator(year)

    print filename
    for i, game in enumerate(soup.find_all("tr", {"height":12})):
        if i == 0:
            continue

        cells = game.find_all("td")

        if i % 2 == 0:
            pg.add_line(Line(cells, year))

            pg.generate_props()

            pg = PropGenerator(year)
        else:
            pg.add_line(Line(cells, year))

###########################################################################
class ExcelLine(Line):
    """a subclass of Line that works from Excel"""
    def __init__(self, cells, year, location):
        mmdd = ('0' + str(cells[0]))[-4:]
        if mmdd[0] == '1':
            year -= 1

        try:
            self.game_date = date(year, int(mmdd[:2]), int(mmdd[2:]))
        except ValueError:
            pass

        self.roto = cells[1]
        if cells[2] == 'x':
            self.location = "N"
        else:
            self.location = location

        self.school_name = cells[3].strip()
        self.school_name = "".join([i for i in self.school_name if 31 < ord(i) < 127])
        self.first_half_score = cells[4]
        self.second_half_score = cells[5]
        self.final_score = cells[6]

        def _half_point_line(number):
            if number == 'pk':
                return 0
            if not number:
                return None
            if number == 'NL':
                return None

            # hack to avoid tickled odds ("3.5-101")
            try:
                number = number.split("-")[0]
            except AttributeError:
                pass

            try:
                return float(number)
            except ValueError:
                # it has the special 1/2 signal
                if len(number) == 1:
                    return 0.5
                return float(number[:-1]) + 0.5

        def half_point_line(number):
            try:
                return _half_point_line(number)
            except:
                return None

        open_prop = half_point_line(cells[7]) # could be spread or total
        self.close = half_point_line(cells[8]) # could be spread or total
        self.close = half_point_line(self.close)

        self.money_line = half_point_line(cells[9])

        self.second_half_prop = half_point_line(cells[10])
        self.second_half_prop = half_point_line(self.second_half_prop)

import openpyxl
def process_excel_files(filename, year):
    pg = PropGenerator(year)
    import wingdbstub

    book = openpyxl.load_workbook(filename)
    sheet = book.get_sheet_by_name("NCAAB")
    row_string = sheet.calculate_dimension()
    for (i, row) in enumerate(sheet.iter_rows(row_string, row_offset=1), 1):
        cells = [c.value for c in row]
        if not any(cells):
            break

        if i % 2 == 0:
            pg.add_line(ExcelLine(cells, year, "H"))
            pg.generate_props()
            pg = PropGenerator(year)
        else:
            pg.add_line(ExcelLine(cells, year, "A"))

        print i, cells[3]

def run():
    import wingdbstub
    import glob
    #for filename in glob.glob("/home/chris/Dropbox/odds/ncaabasketballoddsarchives_*.htm",
                     #):
        #process_file(filename)

    process_excel_files("/home/chris/Dropbox/odds/Master Scores 2014-15a.xlsx",
                        2015)
    print missing_schools
