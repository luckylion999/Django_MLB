from django.core.management.base import BaseCommand
from app.models import * 

class Command(BaseCommand):

    def handle(self, *args, **options):
        ps = PlayerGame.objects.filter(game__id=636).order_by('player__team')
        tt = TeamGame.objects.filter(game__id=636).order_by('team')
        f = open("game_scores.csv", 'w')
        f.write("Team, Player, Points, Projected\n")
        for p in ps:
            f.write("%s,%s,%f,%f\n" % (p.player.team.Name, p.player.Name,p.FantasyPointsFanDuel, p.FantasyPointsFanDuelProjection))
        f.write(",,,\n")
        f.write("Defense Team, Points, Average\n")
        for t in tt:
            f.write("%s,%f,%f\n" % (t.team.Name, t.FantasyPointsFanDuel, t.AverageFantasyPointsFanDuel))
        
        f.close()