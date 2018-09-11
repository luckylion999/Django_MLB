from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
from app.util import make_payments 
 
class Command(BaseCommand):

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument('nfl_start_week')
    
    def handle(self, *args, **options):
        if options['nfl_start_week']:
            make_payments(options['nfl_start_week'])
        else:
            print "nfl_start_week must be provided as an argument"
