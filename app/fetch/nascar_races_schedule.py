import requests
from django.conf import settings
from django.core import serializers
from app.models import (
    NascarRacesSchedule,
) 

def fetch():

    # Note hard coded for 2017 
    uri = "https://api.fantasydata.net/nascar/v3/json/races/2017?key={}".format(settings.FANTASY_DATA_KEY) 
    print uri
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    
    results =  resp.json()
    print results
   
    for result in results: 
        print result
        obj, created = NascarRacesSchedule.objects.get_or_create(
            defaults=result
        )
        print obj 
        #for deserialized_object in serializers.deserialize("json", result):
        #    deserialized_object.save()
     
