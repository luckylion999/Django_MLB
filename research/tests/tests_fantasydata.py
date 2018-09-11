from django.test import TestCase
import requests
import httplib, urllib, base64
from paksite.settings import FANTASY_DATA_KEY
from app.in_parse import *

# http://developer.sportradar.us/apps/register
# Trial key:
srkey = '368794601eb642be822585cb93b8bce6'

class FantasyDataTestCase(TestCase):
      
    def test_players(self):
        uri = 'https://api.fantasydata.net/nfl/v2/{format}/FantasyPlayers?key=%s' % FANTASY_DATA_KEY  
        resp = requests.get(uri)       
        if resp.status_code != 200:
            raise Exception(resp.status_code)
        root = ET.fromstring(resp.text)

        playerdata = root.findall('FantasyPlayer')

        for player in playerdata: 
            prdata, pdata = elem_to_d(APlayer, player)
            player= add_or_get_player(pdata)
            print player
        
        """
        for game in playergames:
            gk = game.findall('GameKey')
            print gk[0].text
            if gk:
                # creating game key but without details
                gameObj, created = Game.objects.get_or_create(GameKey=gk[0].text)
                print game
                update_player_data(list(PlayerAllTags), (game,), gameObj)
        """
         
    def no_test_get_teams(self):

        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/Teams?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
        print_json(resp)


    def no_test_games_in_progress(self):
       
        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/AreAnyGamesInProgress?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
        print_json(resp)
        
        
    def no_test_box_scores(self):
       
        #http://api.nfldata.apiphany.com/nfl/v2/{format}/BoxScores/{season}/{week}
        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/BoxScores/2015PRE/4?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
        print_json(resp)
        
    def no_test_daily_players(self):
       
        #http://api.nfldata.apiphany.com/nfl/v2/{format}/DailyFantasyPlayers/{date}
        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/DailyFantasyPlayers/2015-SEP-03?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
        print_json(resp)

      
    def no_test_active_box(self):
       
        #http://api.nfldata.apiphany.com/nfl/v2/{format}/ActiveBoxScores 
        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/ActiveBoxScores?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
        print_json(resp)

    def no_test_box_score_delta(self):
      
        #http://api.nfldata.apiphany.com/nfl/v2/{format}/BoxScoresDelta/{season}/{week}/{minutes} 
        uri = "http://api.nfldata.apiphany.com/nfl/v2/json/BoxScoresDelta/2015PRE/0/2?key=%s" % srkey 
        print uri

        resp = requests.get(uri)       
        print_json(resp)
        
    