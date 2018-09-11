
from app.models import TournamentSpec, TournamentPlacement

def get_payout(contest, place ):
    tp = TournamentPlacement.objects.get(spec=contest.spec,place=place)  
    return tp.pays
 
