from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
import csv
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        reader = csv.reader(open('app/management/commands/data/Recontact.csv', 'rb'))
        for row in reader:
            name = row[0]
            email = row[1]
            print "{} - {}".format(name, email)
        
                
        #c = Context(locals())
        #t = get_template('updated_scores.txt')
        #txt = t.render(c)
        #print txt