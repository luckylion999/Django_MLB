import xml.etree.cElementTree as ET
from app.models import *
from xml.dom import minidom
from django.test import TestCase
import requests
import httplib, urllib, base64
from paksite.settings import FANTASY_DATA_KEY
 

class TeamDefenseTestCase(TestCase):
    def test_parse(self):
        #https://api.fantasydata.net/nfl/v2/XML/FantasyDefenseByGame/2015/1
        uri = "https://api.fantasydata.net/nfl/v2/XML/FantasyDefenseByGame/2015/1?key=%s" % FANTASY_DATA_KEY 
        print uri

        resp = requests.get(uri)       
       
        if resp.status_code != 200:
            raise Exception(resp.status_code)
     
        print resp.text
     
        items = resp.text
        xml = minidom.parseString(items) # or xml.dom.minidom.parseString(xml_string)
        items = xml.toprettyxml() 

        fname = timezone.localtime(timezone.now()).strftime('%Mdefense-minute-%Hhour')

        f = open('%s.xml.txt' % fname, 'w')
        f.write(str(items))
        f.close()        