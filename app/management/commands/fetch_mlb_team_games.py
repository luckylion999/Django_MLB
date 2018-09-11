from django.core.management.base import BaseCommand
from app.fetch.mlb import Mlb



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--date')

    # date : string  (The date of the game(s). Examples: 2017-JUL-31, 2017-SEP-01.)
    def handle(self, *args, **options):
        Mlb().save_team_games(date=options['date'])
        print options['date']
