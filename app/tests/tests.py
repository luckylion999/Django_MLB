from django.test import TestCase
from app.models import * 
from app.fetch.schedules import *
from app.fetch.rosters import *
from app.fetch.player_projections import *
from app.parse import get_timeframe

class InitCase(TestCase):
    def setUp(self):
       
        get_timeframe()
         
        # load season schedules
        get_schedules()
        # load rosters
        get_rosters()
        
        get_projections()

    def test_loading(self):
        self.assertTrue(Game.objects.all().count() > 0)
        # As of 2015, Tony has only played for one team, Dallas, so should only have one Player entry
        self.assertEquals(Player.objects.filter(Name='Tony Romo').count(), 1)

        # Make sure projections were loaded
        self.assertTrue(PlayerGame.objects.all().count() > 0)

    def test_picking(self):
        week = get_current_week()
        pak = ThreePak.objects.create(user=u, start_week=week)