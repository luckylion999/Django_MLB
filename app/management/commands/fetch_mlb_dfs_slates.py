from django.core.management.base import BaseCommand
from app.fetch.mlb import Mlb


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--date')

    # date : string  (The date of the slates. Examples: 2017-JUL-31, 2017-SEP-01.)
    def handle(self, *args, **options):
        Mlb().save_dfs_slates(date=options['date'])
        print options['date']

