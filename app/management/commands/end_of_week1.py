from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.util import end_of_week1 
from app.models import *

from django.core.management.base import BaseCommand, CommandError

            
class Command(BaseCommand):

    help = 'Sends end of 1st session week email'


    def handle(self, *args, **options):
        end_of_week1()
