from django.db import models

# Create your models here.
class School(models.Model):
    """a college or university that fields a basketball team"""
    abbrev = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    division = models.CharField(max_length=5, null=True, blank=True)
    mascot = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """when saving a school, make sure we have the alias set up for it,
        and teams for every known season as well"""
        super(School, self).save(*args, **kwargs)

        alias, created = SchoolAlias.objects.get_or_create(alias=self.name,
                                                 defaults={"school" : self})
        if not created:
            assert alias.school == self

        # TODO:  do this only when creating a new school
        for season in Season.objects.all():
            team = Team.objects.get_or_create(school=self, season=season)


class SchoolAlias(models.Model):
    alias = models.CharField(max_length=100)
    school = models.ForeignKey(School)

class Season(models.Model):
    """a basketball season.  Note that since seasons run from November
    to March, the 'year' for the season is the closing year.  For example,
    a game played in December 1996 is considered to be in the 1997 season"""
    year = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return u"%s" % self.year

    def save(self, *args, **kwargs):
        super(Season, self).save(*args, **kwargs)

        # make sure that we have a team for each school.
        # TODO:  only do when creating a new season
        for school in School.objects.all():
            team, created = Team.objects.get_or_create(school=school,
                                                       season=self)

class Team(models.Model):
    """the intersection of a school and year.  Note that sometimes people
    refer to 'Duke' as team, but to us, 'Duke' is a school.  'Duke-2001'
    is a 'team'"""
    class Meta:
        unique_together = (('school','season'))

    school = models.ForeignKey(School)
    season = models.ForeignKey(Season)

    def __unicode__(self):
        return u"%s-%s" % (self.school.abbrev, self.season.year)

    def get_ordered_games(self):
        return self.game_set.order_by("-game_date")
    ordered_games = property(get_ordered_games)

    def get_prior_game(self, game_date):
        try:
            season = Season.objects.get(start_date__lte=game_date,
                                        end_date__gte=game_date)
            return self.ordered_games.filter(game_date__lt=game_date,
                                             season=season)[0]
        except IndexError:
            return None

    def get_prior_away_game(self, game_date):
        try:
            return self.ordered_games.filter(game_date__lt=game_date,
                                             location__in=("A","N"))[0]
        except IndexError:
            return None

class Game(models.Model):
    """a match between two teams.  Note that a single game in the real
    world will have two records in this table -- one for home/away, and
    one for away/home.  For our purposes, it is just easier to have
    the duplicated data, but you'll have to filter if you are doing
    statistical analysis."""

    team = models.ForeignKey(Team)
    opponent = models.ForeignKey(Team, related_name="+")
    season = models.ForeignKey(Season)
    game_date = models.DateField()
    location = models.CharField(max_length=1, choices=(("H","Home"),
                                                       ("A","Away"),
                                                       ("N","Neutral")))
    result = models.CharField(max_length=1, null=True, blank=True,
                              choices=(('W', 'Won'),
                                       ('L', 'Lost')))
    points_for = models.IntegerField(null=True, blank=True)
    points_against = models.IntegerField(null=True, blank=True)
    field_goal_pct = models.FloatField(null=True, blank=True)
    free_throw_pct = models.FloatField(null=True, blank=True)
    three_point_pct = models.FloatField(null=True, blank=True)
    ppws = models.FloatField(null=True, blank=True)
    turnover_ratio = models.FloatField(null=True, blank=True)
    to_r = models.FloatField(null=True, blank=True) # not sure what this is
    blocks = models.IntegerField(null=True, blank=True)
    fouls = models.IntegerField(null=True, blank=True)
    offensive_rebounds = models.IntegerField(null=True, blank=True)
    total_rebounds = models.IntegerField(null=True, blank=True)
    steals = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    posessions = models.IntegerField(null=True, blank=True)
    offensive_points_per_posession = models.FloatField(null=True, blank=True)
    defensive_points_per_posession = models.FloatField(null=True, blank=True) # not sure what this is

    def __unicode__(self):
        return "%s vs %s on %s" % (self.team.school.name,
                                   self.opponent.school.name, self.game_date)

    def get_side_proposition(self):
        from odds.models import GameSide
        try:
            return GameSide.objects.get(game=self, class_name="GameSide")
        except GameSide.DoesNotExist:
            return None
    side_proposition = property(get_side_proposition)

    def get_total_proposition(self):
        from odds.models import GameTotal
        try:
            return GameTotal.objects.get(game=self, class_name="GameTotal")
        except GameTotal.DoesNotExist:
            return None
    total_proposition = property(get_total_proposition)

    def get_money_proposition(self):
        from odds.models import GameMoney
        try:
            return GameMoney.objects.get(game=self, class_name="GameMoney")
        except GameMoney.DoesNotExist:
            return None

    def get_defensive_rebounds(self):
        return self.total_rebounds - self.offensive_rebounds
    defensive_rebounds = property(get_defensive_rebounds)
