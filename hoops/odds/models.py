from django.db import models

from games.models import Game
    
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
    value = models.FloatField(null=True, blank=True)
    payoff = models.IntegerField(default=-110)

    TEXT_MAP = {
        1 : "W",
        0 : "P",
        -1 : "L"
    }

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

    def get_result_text(self):
        try:
            return self.TEXT_MAP[self.result]
        except KeyError:
            return None
    result_text = property(get_result_text)

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

    def get_result(self):
        if self.game.points_for is None or self.game.points_against is None:
            return None

        if self.game.points_for + self.value < self.game.points_against:
            return -1

        if self.game.points_for + self.value < self.game.points_against:
            return 0

        return 1
    result = property(get_result)

    def pay(self, wager_amount):
        # if we don't have a score, don't return a multiplier
        if self.game.points_for is None or self.game.points_against is None:
            return None

        # if "team" lost, then they lose
        if self.game.points_for + self.value < self.game.points_against:
            return 0

        # if we pushed, then return the wager
        if self.game.points_for + self.value == self.game.points_against:
            return wager_amount

        return self.pay_win(wager_amount)

class GameTotal(Proposition):
    class Meta:
        proxy = True

    TEXT_MAP = { -1 : 'U',
                 0 : 'P',
                 1 : 'O'}

    def get_result(self):
        if self.game.points_for is None or self.game.points_against is None:
            return None
        if self.game.points_for + self.game.points_against < self.value:
            return -1
        if self.game.points_for + self.game.points_against == self.value:
            return 0
        return 1
    result = property(get_result)

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






