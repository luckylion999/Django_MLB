from django.core.management.base import BaseCommand
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
from app.util import send_my_mail
from datetime import datetime
from django.template import loader, Context
from django.template.loader import get_template
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        dec1 = datetime(month=12,year=2017, day=1, hour=0)
        users = User.objects.filter(date_joined__gt=dec1).order_by('-date_joined')
        data = [] 
        for user in users:
            entry = {}
            entry['user'] = user
            entry['joined'] = "{}".format(user.date_joined.strftime("%b %d"))
            tp = ThreePak.objects.filter(user=user)
            if len(tp):
                entry['picked_players'] = "Has picks"
            else:
                entry['picked_players'] = ""
                
            contests = Contest.objects.filter(threepaks__user=user)
            if len(contests):
                entry['contests'] = "started contest"
            else:
                entry['contests'] = ""
                
            charges = StripeCharge.objects.filter(threepak__user=user)
            if len(charges):
                entry['paid'] = "Paid"
            else:
                entry['paid'] = ""
            data.append(entry)
        
        c = Context(locals())
        t = get_template('analytics.html')
        txt = t.render(c)
        print txt
        recips = ['venable.devin@gmail.com', 'bill.nelson@spinvestment.net', 'mdmnelson@gmail.com', 'ben@gitwitcreative.com']
        for r in recips:
            send_my_mail('User analytics', txt, r, html=txt)
