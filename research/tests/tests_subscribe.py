from django.test import TestCase
import requests
from app.fetch.fantasy_players import get_fantasy_players
from app.fetch.player_data import get_player_data
from app.in_parse import parse_teams, get_current_week
from app.models import *

"""
./manage.py dumpdata --natural-foreign -e contenttypes -e auth.Permission > app/fixtures/app_data.json 

or use keepdb to avoid the hassle 
./manage.py test --keepdb research.tests.tests_subscribe


"""

class PregamePlaybackTestCase(TestCase):
    #fixtures = ['test_users.json','app_data.json', ]
    
    def setUp(self):
        season = '2015' 
        #ThreePak.objects.all().delete()
        #Contest.objects.all().delete()
        
    def test_player_data(self):

        week = get_current_week()
      
        """ 
        1.  Create a three pak for each player with start week
        2.  Create a contest for each tournament type
        """ 
        users = User.objects.filter(username__icontains='@')
        print "users"
        print users
        specs = TournamentSpec.objects.all()
        for s in specs:
            print s
            for u in users:
                print u
                c = Contest.objects.create(spec=s)
                print c
        #get_player_data(week)
        """
        get_player_data(week, 10000, "2015")
        
        paks = ThreePak.objects.all()
        for p in paks:
            print p.total_week_score
        """
       
       