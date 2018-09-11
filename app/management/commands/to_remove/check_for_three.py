from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
from app.parse import get_current_week
from django.core.mail import send_mail
 
class Command(BaseCommand):

    """
       You must have 3 picks to play.  If you don't have them by Sunday at noon, all picks for this week are removed.
       This gets called on Sunday at noon.
    """
    
    def handle(self, *args, **options):
        
        send_mail('check_for_three.py', '1st minute of the 18th hour on Sunday', 'no-reply@3pak-testing.com',
                  ['devin@918.software',], 
                  fail_silently=False )

        """ 
        week = get_current_week()
        print week
         
        paks = ThreePak.objects.filter(contest__isnull=False, start_week=week.Week)
        for pak in paks:
            picks = pak.get_picks(week.Week)
            if len(picks) < 3: 

                msg = "{},\n".format(pak.user.username)
                msg += "There is no time remaining to pick 3pak players, and you do not have 3 players in your lineup."
                msg += "This is a violation of game rules, so we've removed your picks for this week.  If this is the first week of your session, you'll get"
                msg += "a chance to pick again on Wednesday for the 2nd week."

                send_mail('3pak picks removed', msg, 'no-reply@3pak-testing.com',
                          [pak.user.email, 'devin@918.software'], 
                          fail_silently=False )
               
                rpicks = pak.pick_set.filter(threepak__start_week=week.Week)
                for r in rpicks:
                    pak.pick_set.remove(r)

                
        """ 

                 