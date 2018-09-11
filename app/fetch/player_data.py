import requests
import httplib, urllib, base64
import xml.etree.cElementTree as ET
import os
from app.parse import *

def get_player_data(week, mins=3, season=None, **kwargs):
 
    uri = 'https://api.fantasydata.net/v3/nfl/stats/XML/PlayerGameStatsByWeekDelta/%s/%s/%s?key=%s' % (season, week, mins, FANTASY_DATA_KEY)
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
  
    save_result('player_data_', week, mins, season, **kwargs)

    parse_player_data(resp.text)

def get_week_player_data(week, season=None, **kwargs):
 
    uri = 'https://api.fantasydata.net/v3/nfl/stats/XML/PlayerGameStatsByWeek/%s/%s?key=%s' % (season, week,  FANTASY_DATA_KEY)
    print uri
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
  
    parse_player_data(resp.text)



def parse_player_data(res):
    root = ET.fromstring(res)

    playergames = root.findall('PlayerGame')
    print playergames
    for game in playergames:
        print game
        gameObj = update_game_data(GameTags, game) 
        update_player_data(list(PlayerAllTags), (game,), gameObj)
     
        
if __name__=="__main__":
    get_box_scores(2)
