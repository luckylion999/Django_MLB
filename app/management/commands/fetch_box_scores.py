from django.core.management.base import BaseCommand
from app.parse import get_current_week, get_current_timeframe
from app.fetch.box_scores import get_box_scores

class Command(BaseCommand):

    def handle(self, *args, **options):
            
        week = get_current_week()
        tf = get_current_timeframe()
        print "week %s" % week.Week
        #get_box_scores(week, mins=100000, season='2015', save=True)
        get_box_scores(week.Week, season=tf.season_str)
