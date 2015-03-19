from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from django import forms
from games.models import School, Team, Season, Game

schools = School.objects.order_by("name")

class GameForm(forms.Form):
    team = forms.ModelChoiceField(queryset=schools)
    opponent = forms.ModelChoiceField(queryset=schools)
    game_date = forms.DateField()
    points_for = forms.IntegerField()
    points_against = forms.IntegerField()
    
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game_date = form.cleaned_data['game_date']
            
            season = Season.objects.get(start_date__lte=game_date,
                                        end_date__gte=game_date)

            team = Team.objects.get(school=form.cleaned_data['team'],
                                    season=season)
            opponent = Team.objects.get(school=form.cleaned_data['opponent'],
                        season=season)
            points_for = form.cleaned_data['points_for']
            points_against = form.cleaned_data['points_against']
            
            game, created = Game.objects.get_or_create(game_date=game_date,
                    team=team, opponent=opponent, season=season,
                    defaults={"points_for" : points_for,
                              "points_against" : points_against})
            
            if not created:
                game.points_for = points_for
                game.points_against = points_against
    
            game, created = Game.objects.get_or_create(game_date=game_date,
                    team=opponent, opponent=team, season=season,
                    defaults={"points_for" : points_against,
                    "points_against" : points_for})   

            if not created:
                game.points_for = points_against
                game.points_against = points_for
                
            messages.info(request, "changes saved")
            
            return redirect(reverse("games.views.history"))
    else:
        form = GameForm()
        
    return render(request, "add_game.html", {"form" : form})