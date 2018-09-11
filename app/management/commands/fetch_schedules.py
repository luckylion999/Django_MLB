from django.core.management.base import BaseCommand
from app.fetch.schedules import get_schedules
from app.parse import *
from django.core.mail import send_mail

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        """
        Creates Game objects
        """
        tf = get_current_timeframe()
        get_schedules(season='%s' % tf.Season)
        #get_schedules(season='2017PRE')
        get_schedules(season='{}Reg'.format(tf.Season))
        get_schedules(season='{}Post'.format(tf.Season))
