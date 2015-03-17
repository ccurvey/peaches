from django.db import models

from odds.models import Proposition
# Create your models here.

from games.models import Game, Team

class PredictionModel(models.Model):
    name = models.CharField(max_length=100)

    def get_name(self):
        try:
            return self.MODEL_NAME
        except AttributeError:
            return self.__class__.__name__
    name = property(get_name)

class Prediction(models.Model):
    model = models.ForeignKey(PredictionModel)
    game = models.ForeignKey(Game)
    spread = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    money_line = models.IntegerField(null=True, blank=True)

    # these can be gotten either frmo the game, or they can be set
    # dynamically.
    _team = models.ForeignKey(Team, null=True, blank=True, db_column="team_id")
    _opponent = models.ForeignKey(Team, null=True, blank=True,
                                  db_column="opponent_id", related_name="+")
    _game_date = models.DateField(null=True, blank=True, db_column="game_date")

    def get_spread(self):
        return self.opponent_score - self.team_score
    spread = property(get_spread)

    def get_total(self):
        return self.team_score + self.opponent_score
    total = property(get_total)

    def get_team(self):
        if self._team is None:
            self._team = self.game.team
        return self._team
    team = property(get_team)

    def get_opponent(self):
        if self._opponent is None:
            self._opponent = self.game.opponent
        return self._opponent
    opponent = property(get_opponent)

    def get_game_date(self):
        if self._game_date is None:
            self._game_date = self.game.game_date
        return self._game_date
    game_date = property(get_game_date)

    def get_name(self):
        try:
            return self.MODEL_NAME
        except AttributeError:
            return self.__class__.__name__
    name = property(get_name)

#######################################################################
class ReturnToMean(Prediction):
    class Meta:
        proxy = True

    """Assumes that both teams will score the average of their score
       from the prior game and the amount allowed by the other team's
       opponent in the prior game"""
    def get_team_score(self):
        try:
            team_for = self.team.get_prior_game(self.game_date).points_for
            opponent_against = self.opponent.get_prior_game(self.game_date).points_against
        except (AttributeError, TypeError):
            # no prior game
            return None

        return (team_for + opponent_against) / 2
    team_score = property(get_team_score)

    def get_opponent_score(self):
        try:
            team_against = self.team.get_prior_game(self.game_date).points_against
            opponent_for = self.opponent.get_prior_game(self.game_date).points_for
        except (AttributeError, TypeError):
            # no prior game
            return None

        return (opponent_for + team_against) / 2
    opponent_score = property(get_opponent_score)

class ReturnToMeanNeutral(ReturnToMean):
    def get_team_score(self):
        try:
            team_for = self.team.get_prior_away_game(self.game_date).points_for
            opponent_against = self.opponent.get_prior_away_game(self.game_date).points_against
        except (AttributeError, TypeError):
            # no prior game
            return None

        return (team_for + opponent_against) / 2
    team_score = property(get_team_score)

    def get_opponent_score(self):
        try:
            team_against = self.team.get_prior_away_game(self.game_date).points_against
            opponent_for = self.opponent.get_prior_away_game(self.game_date).points_for
        except (AttributeError, TypeError):
            # no prior game
            return None

        return (opponent_for + team_against) / 2
    opponent_score = property(get_opponent_score)

class PointsPerPosession(Prediction):
    class Meta:
        proxy = True

    """Assumes that both teams will keep the same points-per-posession
    averages but that the number of posessions will be the average of the
    number of posessions in the last game for each team"""
    def get_team_score(self):
        team_prior_game = self.team.get_prior_game(self.game_date)
        team_posessions = team_prior_game.posessions
        team_ppp = team_prior_game.offensive_points_per_posession

        opponent_prior_game = self.opponent.get_prior_game(self.game_date)
        opponent_posessions = opponent_prior_game.posessions

        expected_posessions = (team_posessions + opponent_posessions) / 2
        return team_ppp * expected_posessions
    team_score = property(get_team_score)

    def get_opponent_score(self):
        team_prior_game = self.team.get_prior_game(self.game_date)
        team_posessions = team_prior_game.posessions

        opponent_prior_game = self.opponent.get_prior_game(self.game_date)
        opponent_posessions = opponent_prior_game.posessions
        opponent_ppp = opponent_prior_game.offensive_points_per_posession

        expected_posessions = (team_posessions + opponent_posessions) / 2
        return opponent_ppp * expected_posessions
    opponent_score = property(get_opponent_score)

class SideWager(models.Model):
    proposition = models.ForeignKey(Proposition)
    model_name = models.CharField(max_length=100)
    # -1 = loss, 0 = push , 1 = win
    _outcome = models.IntegerField(null=True, blank=True, db_column="outcome")
    predicted_value = models.FloatField()

    def save(self, *args, **kwargs):
        if not self._outcome:
            self.get_outcome()
        super(SideWager, self).save(*args, **kwargs)

    def get_outcome(self):
        if not self._outcome:
            game = self.proposition.game
            proposition = self.proposition

            if game.points_for + proposition.value > game.points_against:
                self._outcome = 1
            elif game.points_for + proposition.value == game.points_against:
                self._outcome = 0
            else:
                self._outcome = -1
        return self._outcome
    outcome = property(get_outcome)

class TotalWager(models.Model):
    proposition = models.ForeignKey(Proposition)
    model_name = models.CharField(max_length=100)
    over_under = models.CharField(max_length=1, choices = (('O','Over'),
                                                           ('U','Under')))
    # -1 = loss, 0 = push , 1 = win
    _outcome = models.IntegerField(null=True, blank=True, db_column="outcome")
    predicted_value = models.FloatField()

    def save(self, *args, **kwargs):
        if not self._outcome:
            self.get_outcome()
        super(TotalWager, self).save(*args, **kwargs)

class OverWager(TotalWager):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.over_under is None:
            self.over_under = 'O'
        super(OverWager, self).save(*args, **kwargs)

    def get_outcome(self):
        if self._outcome is None:
            game = self.proposition.game
            total = game.points_for + game.points_against
            if total == self.proposition.value:
                self._outcome = 0
            elif total > self.proposition.value:
                self._outcome = 1
            else:
                self._outcome = -1
        return self._outcome
    outcome = property(get_outcome)

class UnderWager(TotalWager):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.over_under is None:
            self.over_under = 'U'
        super(OverWager, self).save(*args, **kwargs)

    def get_outcome(self):
        if self._outcome is None:
            game = self.proposition.game
            total = game.points_for + game.points_against
            if total == self.proposition.value:
                self._outcome = 0
            elif total > self.proposition.value:
                self._outcome = -1
            else:
                self._outcome = 1
        return self._outcome
    outcome = property(get_outcome)

class MoneyLineWager(SideWager):
    class Meta:
        proxy = True



