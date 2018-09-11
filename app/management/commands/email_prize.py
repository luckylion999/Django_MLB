from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
from django.core.mail import EmailMessage 
import csv

 
class Command(BaseCommand):

    
    def handle(self, *args, **options):

        # Runs on wednesday, so we need contest ending in last week's week
        now_week, last_week, start_week = Timeframe.get_previous_timeframes()

        print now_week
        print last_week
        print start_week
        
               
        customers = CustomerProfile.objects.filter(name__in=['flying-tee', 'stoneys', 'biggios'])
        for customer in customers:
            print customer
            print '---'
            
            with open('prize_info.csv', 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(('company', 'prize code', 'prize awarded', 'user', 'email'))
                
                text = "'company', 'prize code', 'user', 'email'\n"
                
                paks = ThreePak.objects.filter(
                    start_week=start_week.Week,
                    season_type=start_week.SeasonType,
                    season=start_week.Season,
                    prize_group__gt=0, 
                    user__usercompany__customer=customer)
                try: 
                    contest = paks.first().contest
                    for p in paks:                                                
                        if p.prize_group > 0:
                            text += "{}, {}, {}, {}, {}\n".format(p.user.usercompany.customer.name, p.prize_code, p.prize_text,    p.user.username,p.user.email)
                            writer.writerow((p.user.usercompany.customer.name, p.prize_code, p.prize_text,    p.user.username,p.user.email))
                            
                except:
                    contest = None 
                    
            sendto = ['devin@918.software',
                    # 'sarah@gitwit.com',
                     'bill@3pak.com'
                     ]
            # Send to will@stoneysbarandgrill.com for Stoney's  - per request on Aug 31, 2017
            if customer.name=='stoneys': 
                sendto.append('will@stoneysbarandgrill.com')
                
            if contest:
                email = EmailMessage(
                    '3pak winner codes for {}'.format(contest),
                    'Prize information for {}\n\n{}'.format(contest, text),
                    'devin@918.software',
                    sendto,
                    reply_to=['support-team@3pak.com'],
                    )
                email.attach_file('prize_info.csv')
                email.send(fail_silently=False)
                
