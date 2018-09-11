from django.core.management.base import BaseCommand
from app.models import *
from django.template import loader, Context
from django.template.loader import get_template
from app.parse import send_my_mail

class Command(BaseCommand):

    def handle(self, *args, **options):

        current_week = CurrentWeek.objects.last().Week
        paks = ThreePak.objects.all()
        #parse_player_scores(1, 10800, '2015pre', save=True)
        for pak in paks: 
           
            try: 
                c = Context(locals())
                t = get_template('totals.txt')
                txt = t.render(c)
                print txt
                send_my_mail("3pak score update", txt, pak.user.username)
            except Exception as ex:
                print ex
                print "failed to render"
                print locals()
            
           