from django.core.management.base import BaseCommand
from app.parse import *
import time
from django.template import loader, Context
from django.template.loader import get_template
from app.models import *
from paksite.settings import STRIPE_LIVE_SECRET 
import stripe
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        stripe.api_key =  STRIPE_LIVE_SECRET
        
        all = StripeToken.objects.filter(recipient_id="")
        for tk in all:
            if tk.customer_id:
                try:
                    cs = stripe.Customer.retrieve(tk.customer_id)
                    print cs
                    print cs.description
                    print cs.default_source
                    print cs.sources.data[0].name
                   
                    rec = stripe.Recipient.create(
                          name=cs.sources.data[0].name,
                          type="individual",
                          email=cs.description,
                          card=cs.sources.data[0].id)
                    
                    tk.recipient_id = rec.id
                    tk.save()
                except Exception as ex:
                   print ex.message 