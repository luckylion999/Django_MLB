import requests
from django.conf import settings
from django.core import serializers
from app.models import (
    NascarSeries,
    League
) 

def fetch():
  
    # Ensure leage is present
    league, created = League.objects.get_or_create(name='NASCAR')
    
    uri = "https://api.fantasydata.net/nascar/v3/json/series?key={}".format(settings.FANTASY_DATA_KEY) 
    print uri
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    
    series =  resp.json()
    print series
    for s in series:
        obj, created = NascarSeries.objects.get_or_create(
            league=league,
            SeriesID=s['SeriesID'],
            Name=s['Name']
        )
        print obj 
