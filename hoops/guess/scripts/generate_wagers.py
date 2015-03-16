from odds.models import Proposition

from guess.models import SideWager, ReturnToMean, PointsPerPosession

PREDICTION_MODELS = [ReturnToMean, PointsPerPosession]
def generate_predictions(game):
    return [cls(game=game) for cls in PREDICTION_MODELS]

def generate_sides():
    # so let's say the propositions are:
    # Duke / Maryland, -5
    # Maryland / Duke, +5
    # 
    # if our model says Duke -8, then we bet duke.
    # the other side of the model would say Maryland +8, 
    #   so we don't take that bet.
    #
    # if our model says Duke -1, we don't take that bet
    # the other side would be Maryland +1, and we do take
    #   that bet
    #
    # We only take the bet if the spread we get is smaller
    # (which includes a "bigger negative") than the proposed 
    # spread.    
    import wingdbstub
    for proposition in Proposition.objects.filter(class_name='GameSide'):
        for prediction in generate_predictions(proposition.game):
            if prediction.spread < proposition.value \
               and abs(prediction.spread - proposition.value) > 0.05:
                wager, created = SideWager.objects.get_or_create(
                    proposition=proposition, model_name=prediction.name,
                    predicted_value=prediction.spread)
            
def generate_totals(self):
    for proposition in Proposition.objects.filter(class_name='GameTotal'):
        for prediction in generate_predictions(proposition.game):
            if prediction.total < proposition.value:
                wager, created = UnderWager(proposition=proposition, 
                                            model_name=prediction.name,
                                            predicted_value=prediction.total)
            elif prediction.total > proposition.value:
                    wager, created = OverWager(proposition=proposition, 
                                                model_name=prediction.name,
                                                predicted_value=prediction.total)

def run():
    generate_sides()
    generate_totals(self)