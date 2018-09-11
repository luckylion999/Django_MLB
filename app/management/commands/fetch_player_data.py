from django.core.management.base import BaseCommand
from app.parse import * 
from app.fetch.player_data import * 
from django.core.mail import send_mail

"""
Note that this will never return results until games start.

"""
class Command(BaseCommand):

    def handle(self, *args, **options):
        #send_mail('fetch_player_data.py', '40th minute every hour', 'no-reply@3pak-testing.com',
        #          ['devin@918.software',], 
        #          fail_silently=False )

            
        timeframe = get_current_timeframe()
        week = get_current_week()
        
        get_player_data(week.Week, season=timeframe.season_str)
        get_week_player_data(week.Week, season=timeframe.season_str)
