from django.core.management.base import BaseCommand
from app.fetch.mlb import Mlb


class Command(BaseCommand):
    def handle(self, *args, **options):
        Mlb().create_news()

