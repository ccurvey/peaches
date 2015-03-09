from django.shortcuts import render
from django import forms

from games.models import Team, School, Season

class MatchupForm(forms.Form):
    game_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={"class" : "datepicker"}))
    school1 = forms.ModelChoiceField(queryset=School.objects.order_by("abbrev"))
    school2 = forms.ModelChoiceField(queryset=School.objects.order_by("abbrev"))
    spread = forms.FloatField()
    total = forms.FloatField()

# TODO:  move the prediction models out to their own app so that we can do
# more stuff with them.
class PredictionModel(object):
    def __init__(self, team1, team2, game_date):
        self.team1 = team1
        self.team2 = team2
        self.game_date = game_date

    def get_name(self):
        try:
            return self.MODEL_NAME
        except AttributeError:
            return self.__class__.__name__
    name = property(get_name)

    def get_spread(self):
        return self.team2_score - self.team1_score
    spread = property(get_spread)

    def get_total(self):
        return self.team1_score + self.team2_score
    total = property(get_total)

class ReturnToMean(PredictionModel):
    """Assumes that both teams will score the average of their score
       from the prior game and the amount allowed by the other team's
       opponent in the prior game"""
    def get_team1_score(self):
        team1_for = self.team1.get_prior_game(self.game_date).points_for
        team2_against = self.team2.get_prior_game(self.game_date).points_against

        return (team1_for + team2_against) / 2
    team1_score = property(get_team1_score)

    def get_team2_score(self):
        team1_against = self.team1.get_prior_game(self.game_date).points_against
        team2_for = self.team2.get_prior_game(self.game_date).points_for

        return (team2_for + team1_against) / 2
    team2_score = property(get_team2_score)

class PointsPerPosession(PredictionModel):
    """Assumes that both teams will keep the same points-per-posession
    averages but that the number of posessions will be the average of the
    number of posessions in the last game for each team"""
    def get_team1_score(self):
        team1_prior_game = self.team1.get_prior_game(self.game_date)
        team1_posessions = team1_prior_game.posessions
        team1_ppp = team1_prior_game.offensive_points_per_posession

        team2_prior_game = self.team2.get_prior_game(self.game_date)
        team2_posessions = team2_prior_game.posessions
        #team2_ppp = team2_prior_game.offensive_points_per_posession

        expected_posessions = (team1_posessions + team2_posessions) / 2
        return team1_ppp * expected_posessions
    team1_score = property(get_team1_score)

    def get_team2_score(self):
        team1_prior_game = self.team1.get_prior_game(self.game_date)
        team1_posessions = team1_prior_game.posessions
        #team1_ppp = team1_prior_game.offensive_points_per_posession

        team2_prior_game = self.team2.get_prior_game(self.game_date)
        team2_posessions = team2_prior_game.posessions
        team2_ppp = team2_prior_game.offensive_points_per_posession

        expected_posessions = (team1_posessions + team2_posessions) / 2
        return team2_ppp * expected_posessions
    team2_score = property(get_team2_score)

"""This works if you have an existing line.  If you don't, use the one below"""
class MarketPrediction(PredictionModel):
    def get_team1_score(self):
        import wingdbstub

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

class MarketPrediction(PredictionModel):
    def __init__(self, team1, team2, game_date, spread, total):
        super(MarketPrediction, self).__init__(team1, team2, game_date)
        self._spread = spread
        self._total = total

    def get_team1_score(self):
        return (self._total / 2) - (self._spread / 2)
    team1_score = property(get_team1_score)

    def get_team2_score(self):
        return (self._total / 2) + (self._spread / 2)
    team2_score = property(get_team2_score)

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
            rtm = ReturnToMean(team1, team2, game_date)
            ppp = PointsPerPosession(team1, team2, game_date)

            return render(request, "preview.html",
                          {"form" : form,  "team1" : team1, "team2" : team2,
                           "models" : (market, rtm, ppp)})
    else:
        form = MatchupForm()

    return render(request, "preview.html", {"form" : form})
