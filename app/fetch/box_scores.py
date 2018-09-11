import requests
import httplib, urllib, base64
import xml.etree.cElementTree as ET
import os
from app.parse import *

def get_box_scores(week, mins=3, season=None, **kwargs):
 
       
    print "fetching box scores"
 
    uri = "https://api.fantasydata.net/v3/nfl/stats/XML/BoxScoresDelta/%s/%s/3?key=%s" % (season, week, FANTASY_DATA_KEY) 
    print uri
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    
    save_result('boxs_', resp.text, week, mins, season, **kwargs)

    parse_results(resp.text)


# DEBUG later...not sure this api working as originally desiged

def parse_results(res):
    root = ET.fromstring(res)

    boxscores = root.findall('BoxScore')
    for boxscore in boxscores:
        print 'got boxscore'
        game = boxscore.findall('Game')
        gameObj = None
        if game:
            gameObj = update_game_data(GameTags, game[0])
        print 'after game'
    
        playerreceiving = boxscore.findall('*/PlayerReceiving')
        if playerreceiving:
            print 'player rec'
            update_player_data(PlayerReceivingTags, playerreceiving, gameObj)
       
        #print boxscore.findall('*/PlayerRushing')
        PlayerRushing = boxscore.findall('*/PlayerRushing')
        print PlayerRushing
        if PlayerRushing:
            print 'player rush'
            update_player_data(PlayerRushingTags, PlayerRushing, gameObj)
         
        PlayerPassing = boxscore.findall('*/PlayerPassing')
        if PlayerPassing:
            print 'player pass'
            update_player_data(PlayerPassingTags, PlayerPassing, gameObj)

        PlayerKickPuntReturns = boxscore.findall('*/PlayerKickPuntReturns')
        if PlayerKickPuntReturns:
            print 'player kick punt returns'
            update_player_data(PlayerKickPuntReturnsTags, PlayerKickPuntReturns, gameObj)

        PlayerKicking = boxscore.findall('*/PlayerKicking')
        if PlayerKicking:
            print 'player kicking'
            update_player_data(PlayerKickingTags, PlayerKicking, gameObj)

        # Look to game record to see which team is Away, which is Home
        """
        AwayFantasyDefense = boxscore.findall('AwayFantasyDefense')
        print AwayFantasyDefense
        if AwayFantasyDefense:
            prdata, pdata = elem_to_d(FantasyDefenseTags, AwayFantasyDefense[0])
            print prdata 

        HomeFantasyDefense = boxscore.findall('HomeFantasyDefense')
        print HomeFantasyDefense
        if HomeFantasyDefense:
            prdata, pdata = elem_to_d(FantasyDefenseTags, HomeFantasyDefense[0])
            print prdata 
        """
     
        
if __name__=="__main__":
    get_box_scores(2)
