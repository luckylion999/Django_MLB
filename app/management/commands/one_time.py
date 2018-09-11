
from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
from django.core.mail import send_mail
 
class Command(BaseCommand):

    
    def do_not_use_handle(self, *args, **options):
        users = {
                ('Velin', 'joshua.staples@flyingteegolf.com'),
                ('Brownbear68', 'rob.snead@flyingteegolf.com'),
                ('Hogie', 'ahogeman@yahoo.com'),
                ('Kayla.brown', 'kayla.henson77@yahoo.com'),
                ('Corkdiesel', 'corkybar282@gmail.com'),
                ('John', 'jvollbrecht81@gmail.com'),
                ('RicketyCrickets', 'mcdanielbo@yahoo.com'),
                ('Enk', 'jeffenkelmann@gmail.com'),
                ('jlauffer11', 'jlauffer11@msn.com'),
                ('ellefant85', 'ellefant85@gmail.com'),
                ('TwinsVikes', 'cllarson_@myway.com'),
                ('JamesV', 'James@flyingteegolf.com'),
                ('akabickle', 'akabickle@hotmail.com'),
                ('Craycray', 'Kayla.brown@flyingteegolf.com'),
                ('X-Man', 'superbikeckes@gmail.com'),
                ('XMan', 'superbikeckes@gmail.com'),
                ('TenaciousB', 'superbikeckes@gmail.com'),
                ('Flyballer', 'Kayla.henson77@yahoo.com'),
                ('HessyBear', 'ryan.hess@live.com'),
                ('Brinny12', 'nsball9@yahoo.com'),
                ('CheekyMonkeigh', 'bravistadgley@gmail.com'),
                ('Polish_Hammers', 'david@shraderlaw.com'),
                } 
        for u in users:
            msg = """Dear {}, 
            
Unfortunately due to a system error, players that were selected in week 2 were compromised.  We are investigating the error now. Not all of the rosters for all users can be recovered, so we will need to reset everyone to equal points on Tuesday afternoon.  The contest will resume with week 3 picks on Tuesday afternoon and conclude at the end of week 3.
            
3PAK regrets the inconvenience to all users affected.  As a result, if you select a new PAK for week 3, 3PAK will send you a redemption code for a $25 dollar gift card for the inconvenience.  This gift card will be in addition to the normal prizes awarded after week 2-3 contest.  This way, even if your PAK doesn't finish in the top 3, you will at least receive a $25 dollar gift card complements of 3PAK. 
            
Thank you for your patience; if you have any questions, please email us at support@play3pak.com. 
            """.format(u[0])
            send_mail('Week 2 Update - System Error', msg, 'no-reply@3pak-testing.com',
                      [u[1],'devin@918.software'], 
                  fail_silently=False )
