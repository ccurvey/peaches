import os.path
from datetime import date

from bs4 import BeautifulSoup
from fuzzywuzzy import process

import django
django.setup()

from games.models import School, Game, Team, Season, SchoolAlias
from odds.models import BettingLine

ALL_SCHOOLS = [s.name for s in School.objects.all()]
MISSING_SCHOOLS = set()

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
        self.name = cells[3].get_text().strip()
        self.first_half_score = cells[4].get_text()
        self.second_half_score = cells[5].get_text()
        self.final_score = cells[6].get_text().strip()
        open_prop = cells[7].get_text() # could be spread or total
        self.close_prop = cells[8].get_text() # could be spread or total
        if self.close_prop == 'pk':
            self.close_prop = 0
        elif self.close_prop == "NL":
            self.close_prop = None
        else:
            self.close_prop = float(self.close_prop)
        homemoney_line = cells[9].get_text()

        self.second_half_prop = cells[10].get_text()
        if self.second_half_prop == 'pk':
            self.second_half_prop = 0
        elif self.second_half_prop == "NL":
            self.second_half_prop = None
        else:
            self.second_half_prop = float(self.second_half_prop)

    def get_school(self):
        try:
            return School.objects.get(name=self.name)
        except School.DoesNotExist, e:
            try:
                alias = SchoolAlias.objects.get(alias=self.name)
                return alias.school
            except SchoolAlias.DoesNotExist:
                MISSING_SCHOOLS.add(self.name)
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

class PropGenerator(object):
    """starts with two lines and generates all possible propositions
       * home spread (game)
       * home spread (2nd half)
       * away spread (game)
       * away spread (2nd half)
       * total (game)
       * total (2nd half)
    """
    def __init__(self, visitor_line, home_line):
        self.visitor_line = visitor_line
        self.home_line = home_line

def process_file(filename):
    import wingdbstub
    soup = BeautifulSoup(open(filename, "r"))

    (f, ext) = os.path.splitext(filename)
    year = int(f[-4:])
    for i, game in enumerate(soup.find_all("tr", {"height":12})):
        if i == 0:
            continue

        cells = game.find_all("td")

        if i % 2 == 0:
            # second line of couplet
            home_line = Line(cells, year)

            ###########################################################
            ## now we have the home and visitor information, so we
            ## can find the game records and update them
            ###########################################################
            visitor = visitor_line.team
            home = home_line.team

            try:
                visitor_game = Game.objects.get(team=visitor, opponent=home,
                    game_date = visitor_line.game_date)
            except Game.DoesNotExist:
                print "could not find %s at %s on %s" % (visitor_line.name,
                                      home_line.name, visitor_line.game_date)

                """
                try:
                    visitor_name = School.objects.get(name=visitor_line.name)
                except School.DoesNotExist:
                    print "No School %s" % visitor_line.name

                try:
                    home_name = School.objects.get(name=home_line.name)
                except School.DoesNotExist:
                    print "No School %s" % home_line.name
                """
        else:
            visitor_line = Line(cells, year)

def run():
    import glob
    for filename in glob.glob("/home/chris/Dropbox/odds/ncaabasketballoddsarchives_*.htm",
                     ):
        process_file(filename)
    print MISSING_SCHOOLS

