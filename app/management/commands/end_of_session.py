from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.util import end_of_session
from app.models import *

from django.core.management.base import BaseCommand, CommandError

            
class Command(BaseCommand):

    help = 'Calculates results and sends end of session emails. Send Wednesday morning prior to email_prize.'

    def handle(self, *args, **options):
        end_of_session()
