from django.test import TestCase
import pytest

from guess.models import SideWager, OverWager, UnderWager
from games.models import Game, Team, Season, School
from odds.models import GameSide, GameTotal

# Create your tests here.
class WagerTest(TestCase):
    def setUp(self):
        self.duke = School(abbrev="DUKE", name="Duke")
        self.maryland = School(abbrev="MARY", name="Maryland")
        self.season = Season(year=2012, start_date="2011-11-01", 
                             end_date="2012-04-15")
        self.duke_2012 = Team(school=self.duke, season=self.season)
        self.maryland_2012 = Team(school=self.maryland, season=self.season)
        self.game = Game(team=self.duke_2012, opponent=self.maryland_2012)
     
class SideWagerTest(WagerTest):
    def setUp(self):
        super(SideWagerTest, self).setUp()
        self.game_side = GameSide(game=self.game, value=-10)
        self.wager = SideWager(proposition=self.game_side)
        
    def test_win(self):
        self.game.points_for = 75
        self.game.points_against = 60
        
        assert self.wager.outcome == 1

    def test_loss(self):
        self.game.points_for = 65
        self.game.points_against = 60
        
        assert self.wager.outcome == -1
        
    def test_push(self):
        self.game.points_for = 70
        self.game.points_against = 60
        
        assert self.wager.outcome == 0   
        
class OverWagerTest(WagerTest):
    def setUp(self):
        super(OverWagerTest, self).setUp()
        self.over = GameTotal(game=self.game, value=125)
        self.wager = OverWager(proposition=self.over)
        
    def test_over_win(self):
        self.game.points_for = 70
        self.game.points_against = 60
        
        assert self.wager.outcome == 1
    
    def test_over_loss(self):
        self.game.points_for = 62
        self.game.points_against = 60
        
        assert self.wager.outcome == -1
    
    def test_over_push(self):
        self.game.points_for = 62
        self.game.points_against = 63
        
        assert self.wager.outcome == 0        
         
class UnderWagerTest(WagerTest):
    def setUp(self):
        super(UnderWagerTest, self).setUp()
        self.over = GameTotal(game=self.game, value=125)
        self.wager = UnderWager(proposition=self.over)

    def test_under_loss(self):
        self.game.points_for = 70
        self.game.points_against = 60
        
        assert self.wager.outcome == -1
    
    def test_under_win(self):
        self.game.points_for = 62
        self.game.points_against = 60
        
        assert self.wager.outcome == 1
    
    def test_under_push(self):
        self.game.points_for = 62
        self.game.points_against = 63
        
        assert self.wager.outcome == 0        
    