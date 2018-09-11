from django.core.management.base import BaseCommand
from app.parse import parse_teams, get_current_timeframe

class Command(BaseCommand):

    def handle(self, *args, **options):
        tf = get_current_timeframe()
        parse_teams(tf.SeasonType)
