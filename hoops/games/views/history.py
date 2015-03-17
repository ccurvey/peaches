from django.shortcuts import render
from django import forms

from games.models import Team, Season, School

class MatchupForm(forms.Form):
    season = forms.ModelChoiceField(queryset=Season.objects.order_by("-year"))
    school1 = forms.ModelChoiceField(queryset=School.objects.order_by("abbrev"))
    school2 = forms.ModelChoiceField(queryset=School.objects.order_by("abbrev"))

class ComparisonGrid(object):
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.games = {}

    def add_team1_game(self, game):
        self.games[game.game_date] = [game, None]

    def add_team2_game(self, game):
        try:
            self.games[game.game_date][1] = game
        except KeyError:
            self.games[game.game_date] = [None, game]

    def __iter__(self):
        self.play_dates = list(reversed(sorted(self.games.keys())))
        self.play_index = -1

        return self

    def next(self):
        try:
            self.play_index += 1
            return self.play_dates[self.play_index], \
                   self.games[self.play_dates[self.play_index]]
        except IndexError:
            raise StopIteration()

def build_comparison(team1, team2):
    comparison_grid = ComparisonGrid(team1, team2)

    team1_opponents = set()
    for game in team1.ordered_games:
        team1_opponents.add(game.opponent)
        comparison_grid.add_team1_game(game)

    team2_opponents = set()
    for game in team2.ordered_games:
        team2_opponents.add(game.opponent)
        comparison_grid.add_team2_game(game)

    common_opponents = team1_opponents.intersection(team2_opponents)

    return comparison_grid, common_opponents

def history(request):
    if request.REQUEST.has_key("school1"):
        form = MatchupForm(request.POST)
        if form.is_valid():
            team1 = Team.objects.get(
                school=form.cleaned_data['school1'],
                season=form.cleaned_data['season'])
            team2 = Team.objects.get(
                school=form.cleaned_data['school2'],
                season=form.cleaned_data['season'])

            comparison_grid, common_opponents = build_comparison(team1, team2)

            return render(request, "history.html",
                          {"form" : form,  "team1" : team1, "team2" : team2,
                           "comparison_grid" : comparison_grid,
                           "common_opponents" : common_opponents})
    else:
        form = MatchupForm()

    return render(request, 'history.html', {"form" : form})
