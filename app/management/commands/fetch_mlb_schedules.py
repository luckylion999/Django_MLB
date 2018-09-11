from django.core.management.base import BaseCommand
from app.fetch.mlb import MlbScore


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--season')

    # season : string  (Year of the season (with optional season type). Examples: 2018, 2018PRE, 2018POST, 2018STAR,
    #  2019, etc.)
    def handle(self, *args, **options):

        print options['season']
        MlbScore().save_schedules(season=options['season'])
