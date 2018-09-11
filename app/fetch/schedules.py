import requests
import httplib, urllib, base64
import xml.etree.cElementTree as ET
import os
from app.parse import *

# TODO - schedule season needs to be dynamic
def get_schedules(season=None, **kwargs):
 
    uri = "https://api.fantasydata.net/v3/nfl/scores/XML/Schedules/%s?key=%s" % (season, FANTASY_DATA_KEY)
    
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
  
    parse_schedules(resp.text)



def parse_schedules(res):
    root = ET.fromstring(res)

    schedules = root.findall('Schedule')
    for schedule in schedules:
        try:
            gameObj = update_game_data(GameTags, schedule) 
            print "{} {} {}".format(gameObj.GameKey, gameObj.SeasonType, gameObj.id)
        except Exception as ex:
            # It's normal to have a missing game key
            None
        
if __name__=="__main__":
    get_schedules()
