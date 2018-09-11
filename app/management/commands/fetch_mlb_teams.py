from django.core.management.base import BaseCommand
from app.fetch.mlb import Mlb


# fetches Active Teams
class Command(BaseCommand):
    def handle(self, *args, **options):
        Mlb().create_teams()

