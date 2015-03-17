from django.shortcuts import render
from django import forms

from games.models import Team, School, Season
from guess.models import ReturnToMean, ReturnToMeanNeutral, PointsPerPosession, Prediction

class MatchupForm(forms.Form):
    game_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={"class" : "datepicker"}))
    school1 = forms.ModelChoiceField(queryset=School.objects.order_by("name"))
    school2 = forms.ModelChoiceField(queryset=School.objects.order_by("name"))
    spread = forms.FloatField()
    total = forms.FloatField()

"""This works if you have an existing line.  If you don't, use the one below"""
class MarketPrediction(Prediction):
    def get_team1_score(self):
        from games.models import Game
        try:
            game = Game.objects.get(team=self.team1, opponent=self.team2,
                                    game_date=self.game_date)
        except Game.DoesNotExist:
            return None

        # see if there is actually a line for this game
        from odds.models import GameSide, GameTotal
        try:
            side = GameSide.objects.get(game=game, class_name="GameSide")
        except GameSide.DoesNotExist:
            return None

        try:
            total = GameTotal.objects.get(game=game, class_name="GameTotal")
        except GameTotal.DoesNotExist:
            return None

        return (total.value / 2) - (side.value / 2)
    team1_score = property(get_team1_score)

    def get_team2_score(self):
        from games.models import Game
        try:
            game = Game.objects.get(team=self.team2, opponent=self.team1,
                                    game_date=self.game_date)
        except Game.DoesNotExist:
            return None

        # see if there is actually a line for this game
        from odds.models import GameSide, GameTotal
        try:
            side = GameSide.objects.get(game=game, class_name="GameSide")
        except GameSide.DoesNotExist:
            side = None

        try:
            total = GameTotal.objects.get(game=game, class_name="GameTotal")
        except GameTotal.DoesNotExist:
            total = None

        if side and total:
            return (total.value / 2) - (side.value / 2)
    team2_score = property(get_team2_score)

class MarketPrediction(Prediction):
    def __init__(self, team, opponent, game_date, spread, total):
        super(MarketPrediction, self).__init__()
        self._game_date = game_date
        self._team = team
        self._oppponent = opponent
        self._spread = spread
        self._total = total

    def get_team_score(self):
        return (self._total / 2) - (self._spread / 2)
    team_score = property(get_team_score)

    def get_opponent_score(self):
        return (self._total / 2) + (self._spread / 2)
    opponent_score = property(get_opponent_score)

# Create your views here.
def preview(request):
    if request.REQUEST.has_key("school1"):
        form = MatchupForm(request.POST)

        if form.is_valid():
            season = Season.objects.get(
                start_date__lte = form.cleaned_data['game_date'],
                end_date__gte = form.cleaned_data['game_date'])

            team1 = Team.objects.get(
                school=form.cleaned_data['school1'], season=season)
            team2 = Team.objects.get(
                school=form.cleaned_data['school2'], season=season)
            game_date = form.cleaned_data['game_date']

            market = MarketPrediction(team1, team2, game_date,
                                      form.cleaned_data['spread'],
                                      form.cleaned_data['total'])
            import wingdbstub
            rtm = ReturnToMean(_team=team1, _opponent=team2,
                               _game_date=game_date)
            ## commented out until next season
            ##rtm_n = ReturnToMeanNeutral(_team=team1, _opponent=team2,
                                        ##_game_date=game_date)
            ppp = PointsPerPosession(_team=team1, _opponent=team2,
                                     _game_date=game_date)

            return render(request, "preview.html",
                          {"form" : form,  "team1" : team1, "team2" : team2,
                           "models" : (market, rtm, ppp)})
    else:
        form = MatchupForm()

    return render(request, "preview.html", {"form" : form})
