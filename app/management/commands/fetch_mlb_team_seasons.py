from django.core.management.base import BaseCommand
from app.fetch.mlb import Mlb


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--season')

    def handle(self, *args, **options):
        # season : string  (Year of the season. Examples: 2017, 2018.)

        Mlb().save_team_seasons(season=options['season'])
