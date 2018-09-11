from django.test import TestCase
import requests

srkey = '368794601eb642be822585cb93b8bce6'
import xml.sax

class PlayerReceivingHandler( xml.sax.ContentHandler ):

    mapp = {}
    tag = ""
    
    def startElement(self, name, attrs):
        if name == "PlayerReceiving":
            self.mapp[name] = ''
            self.tag = name

    def characters(self, content):
        if self.tag == "PlayerReceiving":
            self.mapp[self.tag] += content

    def endElement(self, name):
        if self.tag == "PlayerReceiving":
            print self.mapp[self.tag]
        
    # Call when an element starts
    #def startElement(self, tag, attributes):
    #    self.CurrentData = tag
    #    if tag == "PlayerReceiving":
    #        print "*****PlayerReceiving*****"
    #        print ["%s,%s" % (x, x.getValue()) for x in attributes.getNames()]
         
class SaxParseTestCase(TestCase):
      
       
    def test_parse(self):
      
        #uri = "http://api.fantasydata.net/nfl/v2/xml/BoxScoresDelta/2015PRE/4/2?key=%s" % srkey 
        #resp = requests.get(uri)       
       
        #if resp.status_code != 200:
        #    raise Exception(resp.status_code)
    
        f = 'data/xmlsep4/00minute-01hour.xml'
      
        handler = PlayerReceivingHandler()
        xml.sax.parse(f, handler)