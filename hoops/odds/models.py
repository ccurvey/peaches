from django.db import models

from games.models import Game

class PredictionModel(models.Model):
    name = models.CharField(max_length=100)

    def get_name(self):
        try:
            return self.MODEL_NAME
        except AttributeError:
            return self.__class__.__name__
    name = property(get_name)

    def get_spread(self, team1, team2, game_date):
        team1_score = self.get_team_score(team1, team2, game_date)
        team2_score = self.get_team_score(team2, team1, game_date)
        return team1_score - team2_score
    spread = property(get_spread)

    def get_total(self, team1, team2, game):
        team1_score = self.get_team_score(team1, team2, game_date)
        team2_score = self.get_team_score(team2, team1, game_date)
        return team1_score + team2_score
    total = property(get_total)

class Prediction(models.Model):
    model = models.ForeignKey(PredictionModel)
    game = models.ForeignKey(Game)
    spread = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    money_line = models.IntegerField(null=True, blank=True)

#########################################################################
class ReturnToMean(PredictionModel):
    """Assumes that both teams will score the average of their score
       from the prior game and the amount allowed by the other team's
       opponent in the prior game"""
    def get_team_score(self, team1, team2, game_date):
        team1_for = self.team1.get_prior_game(self.game_date).points_for
        team2_against = self.team2.get_prior_game(self.game_date).points_against

        return (team1_for + team2_against) / 2
    team_score = property(get_team_score)

###########################################################################
class PointsPerPosession(PredictionModel):
    """Assumes that both teams will keep the same points-per-posession
    averages but that the number of posessions will be the average of the
    number of posessions in the last game for each team"""
    def get_team_score(self, team1, team2, game_date):
        team1_prior_game = self.team1.get_prior_game(self.game_date)
        team1_posessions = team1_prior_game.posessions
        team1_ppp = team1_prior_game.offensive_points_per_posession

        team2_prior_game = self.team2.get_prior_game(self.game_date)
        team2_posessions = team2_prior_game.posessions

        expected_posessions = (team1_posessions + team2_posessions) / 2
        return team1_ppp * expected_posessions
    team_score = property(get_team_score)

#########################################################################
class BettingLine(models.Model):
    game = models.ForeignKey(Game)
    line_type = models.CharField(max_length=1,
                                 choices=(('S', 'Spread'),
                                          ('T', 'Total'),
                                          ('M', 'Money')))
    odds = models.FloatField(default=-110)

class Proposition(models.Model):
    game = models.ForeignKey(Game)
    class_name = models.CharField(max_length=100)
    value = models.FloatField()
    payoff = models.IntegerField(default=-110)

    def save(self, *args, **kwargs):
        if not self.class_name:
            self.class_name == self.__class__.__name__
        super(Proposition,self).save(*args, **kwargs)

    def pay_win(self, wager_amount):
        if self.payoff > 0:
            return wager_amount + (wager_amount * (float(self.payoff) / 100))

        if self.payoff < 0:
            return wager_amount + (wager_amount * -100 / float(self.payoff))

        # if it was even money, then return double the wager
        return 2 * wager_amount

class GameMoney(Proposition):
    """straight up"""
    class Meta:
        proxy = True

    def pay(self, wager_amount):
        # if we don't have a score, don't return a multiplier
        if self.game.points_for is None or self.game.points_against is None:
            return None

        # if "team" lost, then they lose on the money line
        if self.game.points_for < self.game.points_against:
            return 0

        # if we pushed, then return the wager
        if self.game.points_for == self.game.points_against:
            return wager_amount

        # if "team" won, then we have to look at the sign of the payoff
        return self.pay_win(wager_amount)

class GameSide(Proposition):
    """against the spread"""
    class  Meta:
        proxy = True

    def pay(self, wager_amount):
        # if we don't have a score, don't return a multiplier
        if self.game.points_for is None or self.game.points_against is None:
            return None

        # if "team" lost, then they lose on the money line
        if self.game.points_for + self.value < self.game.points_against:
            return 0

        # if we pushed, then return the wager
        if self.game.points_for + self.value == self.game.points_against:
            return wager_amount

        return self.pay_win(wager_amount)

class GameTotal(Proposition):
    class Meta:
        proxy = True

    def pay(self, wager_amount):
        if self.game.points_for is None or self.game.points_against is None:
            return None

        # loss
        if self.game.points_for + self.game.points_against < self.value:
            return 0

        # push
        if self.game.points_for + self.game.points_against == self.value:
            return wager_amount

        return self.pay_win(wager_amount)

##########################################################################
## these have to wait until we get half scores
##class HalfSide(Proposition):
    ##class Meta:
        ##proxy = True

##class HalfTotal(Proposition):
    ##class Meta:
        ##proxy = True
##########################################################################

class Wager(models.Model):
    proposition = models.ForeignKey(Proposition)
    wager_amount = models.FloatField()
    _payoff_amount = models.FloatField(null=True, blank=True,
                                       db_column="payoff_amount")

    def get_payoff_amount(self):
        if self._payoff_amount is None:
            self._payoff_amount = self.proposition.pay(self.wager_amount)
        return self._payoff_amount
    payoff_amount = property(get_payoff_amount)






