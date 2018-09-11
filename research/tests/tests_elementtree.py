import xml.etree.cElementTree as ET
from django.test import TestCase
from app.models import *

class ETTestCase(TestCase):
    def test_parse(self):
        f = 'data/xmlsep4/00minute-01hour.xml'
        count = 0
        for event, elem in ET.parse(f):
            if event == 'end':
                d = {}
                if elem.tag == 'Game':
                    print 'processing game'
                    gs = {}
                    usetags = ('GameKey', 'Date', 'AwayTeam', 'HomeTeam', 'SeasonType', 'Season','Week','Stadium')
                    for e in elem.iter():
                        if e.tag in usetags:
                            gs[e.tag]=e.text
                    if gs.has_key('GameKey'):
                        print 'gamekey %s' % gs['GameKey']
                        game = Game.objects.get_or_create(**gs)
                    elem.clear()
                if elem.tag == 'PlayerReceiving':
                    count+=1
                    for e in elem.iter():
                        if e.text:
                            d[e.tag] = e.text
                    elem.clear()
                    #print d
                     
                    gameid= d['PlayerGameID']
                    if not Game.objects.filter(GameKey=gameid):
                        print "we need to load the game"
        print count
        print "Total Game objects"
        print Game.objects.all()
