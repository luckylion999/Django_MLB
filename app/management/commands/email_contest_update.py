from django.core.management.base import BaseCommand
from app.parse import *
from app.signals import send_my_mail 
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
    
class Command(BaseCommand):

    def handle(self, *args, **options):

        """
        Thoughts about joining Contest and ThreePak...

        It's a one to one relationship, so my modeling is off

        Since its one to one, might as well be a single table
        """

        ts = TournamentSpec.objects.all()

        for t in ts:
            contests = Contest.objects.filter(spec=t)
            for c in contests:
                c = Contest.objects.filter(spec=t).first()
                #print c
                pak = ThreePak.objects.filter(contest=c).first()
                #print pak
                #print pak.total_session_score
                
                ss = c.sorted_by_position() 
                # temp return string for now     
                infostr = ""
                for idx in range(0, len(ss)):
                     infostr += "%s is in position %d with %s points\n" % (ss[idx].user.username, (idx+1), ss[idx].total_session_score)
                infostr
                
                c = Context(locals())
                t = get_template('updated_scores.txt')
                txt = t.render(c)
                print txt


"""
        while True:

            print "sleep for 90 minutes"          
            time.sleep(60 * 90)
            
            print "Game in progress...?"
            if game_in_progress():
                print "game on..."
                
                week = get_current_week().Week
                
                paks = ThreePak.objects.filter(start_week__in=(week,int(week)-1)).exclude(ended=True)
                
                contests = Contest.objects.filter(threepaks__in=paks).distinct()
                for contest in contests:
                   
                    ss = contest.sorted_by_position() 
                    # temp return string for now     
                    infostr = ""
                    for idx in range(0, len(ss)):
                         infostr += "%s is in position %d with %s points\n" % (ss[idx].user.username, (idx+1), ss[idx].total_session_score)
                    infostr
                    
                    c = Context(locals())
                    t = get_template('updated_scores.txt')
                    txt = t.render(c)
                  
                    paks = contest.threepaks.all()
                    for pak in paks:              
                        print 'mailing to %s' %  pak.user.username
                        send_my_mail('Latest contest scores', txt, pak.user.username)
               
"""