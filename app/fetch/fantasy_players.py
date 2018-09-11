import requests
import httplib, urllib, base64
import xml.etree.cElementTree as ET
import os
from app.parse import *


def get_fantasy_players():
   
    print "fetching fantasy players"

    uri = 'https://api.fantasydata.net/v3/nfl/stats/xml/FantasyPlayers?key=%s' % FANTASY_DATA_KEY
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    root = ET.fromstring(resp.text)

    playerdata = root.findall('FantasyPlayer')

    for player in playerdata: 
        prdata, pdata = elem_to_d(APlayer, player)
        player= add_or_get_player(pdata)
        
if __name__=="__main__":
    get_fantasy_players()
