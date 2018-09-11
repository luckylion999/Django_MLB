from django.core.management.base import BaseCommand
from app.fetch.news import get_news 

class Command(BaseCommand):

    def handle(self, *args, **options):
        get_news() 