import xml.etree.cElementTree as ET
from app.models import *
from xml.dom import minidom
from django.test import TestCase
import requests
import httplib, urllib, base64

srkey = '368794601eb642be822585cb93b8bce6'

class ETTestCase(TestCase):
    def test_parse(self):
        #https://api.fantasydata.net/nfl/v2/{format}/PlayerGameStatsByWeekDelta/{season}/{week}/{minutes}
        uri = "https://api.fantasydata.net/nfl/v2/XML/PlayerGameStatsByWeekDelta/2015pre/4/10000?key=%s" % srkey
        #uri = "http://api.fantasydata.com/nfl/v2/xml/PlayerGameStatsByWeekDelta/2015PRE/4/100?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
       
        if resp.status_code != 200:
            raise Exception(resp.status_code)
     
        print resp.text
     
        items = resp.text
        xml = minidom.parseString(items) # or xml.dom.minidom.parseString(xml_string)
        items = xml.toprettyxml() 

        fname = timezone.localtime(timezone.now()).strftime('player-%M-minute-%Hhour')

        f = open('%s.xml.txt' % fname, 'w')
        f.write(str(items))
        f.close()        