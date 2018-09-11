from django.test import TestCase
import requests

# http://developer.sportradar.us/apps/register
# Trial key:
#srkey = 'e2ka8wfxmpbbdcc64g7bgrc5'

# Reregistered with app 918software
srkey = 'qgxhb9ynaccgr7r47e9k4p6z'

def print_json( resp):
    if resp.status_code != 200:
        raise Exception(resp.status_code)
   
    print resp.json() 
    return resp.json()

def print_xml( resp):
    if resp.status_code != 200:
        raise Exception(resp.status_code)
   
    print resp.text 

class SportRadarTestCase(TestCase):
    def setUp(self):
        None

       
    """
    Parameter Format Notes

    [access_level] = Production (o), Trial (ot)

    [version] = whole number (sequential, starting with the number 1)

    [year] = Year in 4 digit format (YYYY)

    [month] = Month in 2 digit format (MM)

    [day] = Day of month in 2 digit format (DD)

    [format] = xml, json
    """ 

    def test_history(self):
        # Note this seems to fail if ran more than once a day
        
        uri = "http://api.sportradar.us/nfl-ot1/league/2015/09/04/changes.json?api_key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
        print_json(resp)

    
    def test_game_statistics(self):
        game_id = 'b7aeb58f-7987-4202-bc41-3ad9a5b83fa4' 
        #http(s)://api.sportradar.us/nfl-[access_level][version]/games/[game_id]/statistics.[format]?api_key=[your_api_key]
        uri = "http://api.sportradar.us/nfl-ot1/games/%s/statistics.xml?api_key=%s" % (game_id, srkey)
        print uri
        resp = requests.get(uri)       
        print_xml(resp)

 
    def test_league_hierarchy(self):
        uri = "http://api.sportradar.us/nfl-ot1/league/hierarchy.json?api_key=%s" % srkey 
        print uri
        resp = requests.get(uri)       
        if resp.status_code != 200:
            raise Exception(resp.status_code)
        print resp.json() 
 
       
    """
    [access_level] = Production (o), Trial (ot)

    [version] = whole number (sequential, starting with the number 1)

    [player_id] = ID for a given player

    [format] = xml, json
    """ 

    def test_connect(self):
        playerid = "41c44740-d0f6-44ab-8347-3b5d515e5ecf"  # Tom Brady
        uri = "http://api.sportradar.us/nfl-ot1/players/%s/profile.json?api_key=%s" % (playerid, srkey) 
        print uri

        resp = requests.get(uri)       
        if resp.status_code != 200:
            raise Exception(resp.status_code)
        print resp.json() 