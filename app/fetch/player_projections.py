import requests
import httplib, urllib, base64
import xml.etree.cElementTree as ET
import os
from app.parse import *
from django.db.models import Q
from app.parse import *
from datetime import datetime
from django.conf import settings 


def get_projections(season=None, **kwargs):

    week = get_current_week().Week
         
    # Player
    uri = "https://api.fantasydata.net/v3/nfl/projections/XML/PlayerGameProjectionStatsByWeek/%s/%s?key=%s" % (
        season, 
        week, 
        settings.FANTASY_DATA_PROJECTIONS_KEY
    )
 
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)

     
    parse_p(resp.content)

    # Team 
    uri = "https://api.fantasydata.net/v3/nfl/projections/XML/FantasyDefenseProjectionsByGame/%s/%s?key=%s" % (
        season, 
        week, 
        settings.FANTASY_DATA_PROJECTIONS_KEY
    )
    print uri
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)

     
    parse_p(resp.content)

def parse_p(res):
    root = ET.fromstring(res)
    
    prs = root.findall('PlayerGameProjection')
  
    #print prs 
    if len(prs)==0: 
        prs = root.findall('FantasyDefenseGameProjection')
    
    for pr in prs:
        #for e in pr.iter():
        #    print "%s: %s" %(e.tag, e.text)
  
        team = pr.find('Team').text
        GameKey  = pr.find('GameKey').text
        
        # Team data is only different in that there is no player
        try:
            PlayerID = pr.find('PlayerID').text
            Position = pr.find('Position').text
            Name = pr.find('Name').text
        except:
            PlayerID = None
            
        FantasyPointsFanDuel = pr.find('FantasyPointsFanDuel').text
        FanDuelSalary = pr.find('FanDuelSalary').text
        if not FanDuelSalary:
            FanDuelSalary = 4500
      
        #print ET.tostring(pr) 
        print "Player: {} Salary: {}, Points: {}".format(PlayerID, FanDuelSalary, FantasyPointsFanDuel) 
        game = Game.objects.get(GameKey=GameKey)

        if PlayerID:
            player = add_or_get_player(
                                       {
                                        'PlayerID':PlayerID, 
                                        'Team':team,
                                        'Name':Name, 
                                        'Position':Position}
                                       )
            if FanDuelSalary:
                update_offense(player, game, {'FantasyPointsFanDuelProjection': FantasyPointsFanDuel, 'FanDuelSalary': FanDuelSalary}) 
        else: # Team
            team = Team.objects.get(abbr=team)
            update_defense_rec(team, game, {'FanDuelSalary': FanDuelSalary})
