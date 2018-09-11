from django.core.management.base import BaseCommand
from app.fetch.mlb import MlbProjection



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--season')

    # season : string  (Year of the season. Examples: 2017, 2018.)
    def handle(self, *args, **options):

        MlbProjection().save_player_season_projection(season=options['season'])
        print options['season']
