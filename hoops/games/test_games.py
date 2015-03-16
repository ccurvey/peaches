from datetime import date

import pytest
from django.test import TestCase

from games.models import School, SchoolAlias, Team, Season, Game

class SchoolTest(TestCase):
    def test_save_alias(self):
        s = School(name="TestSchool")
        s.save()
        
        alias = SchoolAlias.objects.get(alias="TestSchool")
        
        self.assertEquals(s, alias.school)
        
    def test_save_season(self):
        season, created = Season.objects.get_or_create(year=2012, 
                start_date='2011-11-01', end_date="2012-04-15")
        school, created = School.objects.get_or_create(name="TestSchool2")
        team, created = Team.objects.get_or_create(school=school, season=season)
        self.assertFalse(created)
        
class SeasonTest(TestCase):
    def test_save_team(self):
        school, created = School.objects.get_or_create(name="TestSchool3")
        season, created = Season.objects.get_or_create(year=2013, 
                                start_date='2012-11-01', end_date="2013-04-15")
        team, created = Team.objects.get_or_create(school=school, season=season)
        self.assertFalse(created)
        
class GameTest(TestCase):
    def set_up_game(self):
        self.duke, created = School.objects.get_or_create(
            abbrev="DUKE", name="Duke")
        
        self.maryland, created = School.objects.get_or_create(
            abbrev='MARY', name='Maryland')
        
        self.season, created = Season.objects.get_or_create(
            year=2013, start_date="2012-11-01", end_date='2013-04-15')
    
        # creating the season *should* have created the teams, so now
        # create two games
        self.duke_2013 = self.duke.team_set.get(season__year=2013)
        self.maryland_2013 = self.maryland.team_set.get(season__year=2013)
        
        self.game1, created = Game.objects.get_or_create(
            team=self.duke_2013, opponent=self.maryland_2013, 
            game_date='2013-03-01', season_id=2013)
    
        self.game2, created = Game.objects.get_or_create(
            team=self.duke_2013, opponent=self.maryland_2013, 
            game_date='2013-03-10', season_id=2013)
        
class TeamTest(GameTest):
    def setUp(self):
        self.set_up_game()
        
    #@pytest.mark.django.db
    def test_prior_game(self):
        prior_game = self.duke_2013.get_prior_game(game_date='2013-03-05')
        
        self.assertEquals(prior_game.game_date, date(2013,3, 01))
        
    def test_no_prior_game(self):
        prior_game = self.duke_2013.get_prior_game(game_date='2013-03-01')
        assert prior_game is None
        
class GameTest(GameTest):
    def setUp(self):
        self.set_up_game()
        
    #@pytest.mark.django.db
    def test_defensive_rebounds(self):
        self.game1.total_rebounds = 20
        self.game1.offensive_rebounds = 15
        assert self.game1.defensive_rebounds == 5
        