from django.test import TestCase
from django.utils import timezone
import requests
import httplib, urllib, base64
from tests_sportradar import print_json
import collections
import time
from xml.dom import minidom
from datetime import datetime
from jsonpath_rw import parse
import json

# http://developer.sportradar.us/apps/register
# Trial key:

srkey = '368794601eb642be822585cb93b8bce6'


def keypaths(nested):
    for key, value in nested.iteritems():
        if isinstance(value, collections.Mapping):
            for subkey, subvalue in keypaths(value):
                yield [key] + subkey, subvalue
        else:
            yield [key], value
           
                        
                    
def gen_dict_extract(key, var):
    if hasattr(var,'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result 

class FantasyDataTestCase(TestCase):
       
    def capture_box_score_json(self):
        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/BoxScores/2015PRE/4?key=%s" % srkey 
        print uri
        resp = requests.get(uri)       
        if resp.status_code != 200:
            raise Exception(resp.status_code)
              
        items = resp.json()
        # just standard parse
        print items[0]
        
    def capture_box_score_json_experiment(self):
        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/BoxScores/2015PRE/4?key=%s" % srkey 
        print uri
        resp = requests.get(uri)       
        if resp.status_code != 200:
            raise Exception(resp.status_code)

        #clean it up? load and then return to string
        parsed = json.loads(resp.text)
        tostr = json.dumps(parsed) 
        # attempt raw parse
        jsonpath_expr = parse(tostr)
              
        items = resp.json()
        fname = datetime.now().strftime('%Mminute-%Hhour')

        f = open('%s.json' % fname, 'w')
        f.write(str(items))
        f.close()        

    def test_box_score_delta(self):
      
        #http://api.nfldata.apiphany.com/nfl/v2/{format}/BoxScoresDelta/{season}/{week}/{minutes} 
        uri = "http://api.nfldata.apiphany.com/nfl/v2/xml/BoxScoresDelta/2015PRE/4/2?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
       
        if resp.status_code != 200:
            raise Exception(resp.status_code)
      
        items = resp.text
        xml = minidom.parseString(items) # or xml.dom.minidom.parseString(xml_string)
        items = xml.toprettyxml() 

        fname = timezone.localtime(timezone.now()).strftime('%Mminute-%Hhour')

        f = open('%s.xml.txt' % fname, 'w')
        f.write(str(items))
        f.close()        
        #for i in items: 
        #    print list(keypaths(i))
       
        #gn = gen_dict_extract('FantasyPointsDraftKings', items)
        
        #for i in gn:
        #    print i