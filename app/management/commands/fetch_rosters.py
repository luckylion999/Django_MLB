from django.core.management.base import BaseCommand
from app.fetch.rosters import get_rosters

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        """
        
        get_rosters()