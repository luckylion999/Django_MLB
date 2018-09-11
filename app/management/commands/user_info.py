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
        
        users = User.objects.exclude(email__in=('d@d.com', 'devin@918.software', 'bill@3pak.com')).order_by('usercompany__customer__name')

        with open('user_info.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(('customer', 'username', 'email', '# sessions', 'sessions', '# invites', 'invited'))
                                                            
            for u in users:                                                     
                #print "{}, {}, {}".format(u.usercompany.customer.name, u.username, u.email)
                
                # sessions played
                cs = Contest.objects.filter(threepaks__user=u)
                sessions_played = cs.count()
                if sessions_played:
                    sessions_named = ' - '.join( [c.__unicode__() for c in cs])
                    invites = u.invites.all()
                    invites_named = ' - '.join( ["{}".format(i.address) for i in invites])
                    

                    writer.writerow([u.usercompany.customer.name, u.username, u.email, sessions_played, sessions_named, len(invites), invites_named])
                
        

        email = EmailMessage(
            '3pak users',
            'Find users and info attached',
            'devin@918.software',
            ['devin@918.software',
             'sarah@gitwit.com',
             'bill@3pak.com'
             ],
            reply_to=['devin@918.software'],
            )
        email.attach_file('user_info.csv')
        email.send(fail_silently=False)
