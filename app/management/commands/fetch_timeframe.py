from app.parse import get_timeframe
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
        
    def handle(self, *args, **options):
        #send_mail('fetch_timeframe.py', 'Should be sent 10th minute of the 7th and 11th hour', 'no-reply@3pak-testing.com',
        #          ['devin@918.software',], 
        #          fail_silently=False )

        # Gets the current time
        get_timeframe(type="current")
        # Gets all times for future games
        get_timeframe(type="all")
