import requests
import httplib, urllib, base64
import xml.etree.cElementTree as ET
import os
from app.parse import *
from django.db.models import Q
from app.models import Thisweek
from datetime import datetime

def get_rosters(**kwargs):

    uri = 'https://api.fantasydata.net/v3/nfl/stats/XML/Players?key=%s' % (FANTASY_DATA_KEY)
 
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)

    #f = open('players.xml', 'w')
    #f.write(resp.content)
    #f.close()
     
    parse_rosters(resp.content)


def parse_rosters(res):

    missing_teams = []
    thisweek = Thisweek.objects.first()
    root = ET.fromstring(res)
    #print res

    rosters = root.findall('Player')
    for roster in rosters:
        #print ET.tostring(roster)
        """
        <UpcomingGameOpponent>BUF</UpcomingGameOpponent>
        <UpcomingGameWeek>5</UpcomingGameWeek>
        """
        team = roster.find('Team').text
        week = roster.find('UpcomingGameWeek').text
        name = roster.find('Name').text
        PlayerID = roster.find('PlayerID').text
        photourl = roster.find('PhotoUrl').text
        position = roster.find('Position').text
        CurrentStatus = roster.find('CurrentStatus').text
        #print "-%s-" % name
        #print "-%s-" % team
        now = datetime.now()
         
        try:
            league, created = League.objects.get_or_create(name='NFL')
            teamObj, created = Team.objects.get_or_create(abbr=team, league=league)
            
            games = Game.objects.filter(Q(AwayTeam=team)| Q(HomeTeam=team), Week=week, SeasonType=thisweek.SeasonType, Season=thisweek.Season)
            #print "Found {} games".format(len(games))
            if len(games)==0:
                #print "Can't find game for team: {}".format(team) 
                missing_teams.append(name)
            gameObj = games.first()
            #print "Game: {}".format(gameObj)
            pObj, created = Player.objects.get_or_create(PlayerID=PlayerID, team=teamObj)
            
            pObj.PhotoUrl = photourl
            pObj.Name = name 
            pObj.position = position 
            pObj.CurrentStatus = CurrentStatus
            pObj.save()
            pobj, created = PlayerGame.objects.get_or_create(game=gameObj, player=pObj) 
            pobj, created = TeamGame.objects.get_or_create(game=gameObj, team=teamObj) 
        except Exception as ex:
           #print ex 
           None
        
    print "missing"
    print missing_teams
    print len(missing_teams)
if __name__=="__main__":
    get_rosters()
