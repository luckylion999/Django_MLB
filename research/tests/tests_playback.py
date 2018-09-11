from django.test import TestCase
import requests
import httplib, urllib, base64
from tests_sportradar import print_json
import xml.etree.cElementTree as ET
import os
from app.in_parse import * 
from app.fetch.fantasy_players import get_fantasy_players

class PregamePlaybackTestCase(TestCase):
    def setUp(self):
        get_fantasy_players()
             
    def test_playback(self):

        return
        
        for root, dirs, files in os.walk('data/xmlsep4'):
            print root, dirs, files
           
            fs = [] 
            for f in files:
                name = "%s/%s" % (root, f)
                t = os.stat(name).st_mtime
                fs.append((t, name))
                
            # Keeping for record, though this isn't accurate because modify time is out
            # of sync from actual file creation. 
            after = sorted(fs, key=lambda x: x[0] )
            
            # Testing basic diff and logging of records as they come in incrementally
            for a in after:
                #f = open(a[1])
                #str =  f.read()
                #f.close()
                    
                # duplicates functionality from in_parse...making this a limited use test.  I don't want 
                # to refactor the function in in_parse just for this test, so I'm doing evil and copy-pasting
                 
                root = ET.parse(a[1])

                boxscores = root.findall('BoxScore')
                for boxscore in boxscores:
                    game = boxscore.findall('Game')
                    gameObj = None
                    if game:
                        gdata, pdata = elem_to_d(GameTags, game[0]) 
                        if pdata.has_key('GameKey'):
                            gameObj, created = Game.objects.get_or_create(GameKey=pdata['GameKey'])
                            Game.objects.filter(id=gameObj.id).update(**gdata)
                            
                
                    playerreceiving = boxscore.findall('*/PlayerReceiving')
                    if playerreceiving:
                        update_player_data(PlayerReceivingTags, playerreceiving, gameObj)
                        #prdata, pdata = elem_to_d(PlayerReceivingTags, playerreceiving[0])
                        #player= add_or_get_player(pdata)
                        #update_offense(player, gameObj, prdata) 
                      
                        
                   
                    #print boxscore.findall('*/PlayerRushing')
                    PlayerRushing = boxscore.findall('*/PlayerRushing')
                    if PlayerRushing:
                        update_player_data(PlayerRushingTags, PlayerRushing, gameObj)
                     
                    PlayerPassing = boxscore.findall('*/PlayerPassing')
                    if PlayerPassing:
                        update_player_data(PlayerPassingTags, PlayerPassing, gameObj)

                    PlayerKickPuntReturns = boxscore.findall('*/PlayerKickPuntReturns')
                    if PlayerKickPuntReturns:
                        update_player_data(PlayerKickPuntReturnsTags, PlayerKickPuntReturns, gameObj)

                PlayerKicking = boxscore.findall('*/PlayerKicking')
                if PlayerKicking:
                    update_player_data(PlayerKickingTags, PlayerKicking, gameObj)