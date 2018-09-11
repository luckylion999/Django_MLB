import requests
import httplib, urllib, base64
import xml.etree.cElementTree as ET
import os
from app.parse import *
import pytz


def get_defense_by_season(season=None):
    """
    This script pulls aggregate scores for all NFL weeks and calculates averages.
    
    If a Tuesday, then last NFL week is over, but FantasyData still reports week is the former week, so jump ahead one 
    to load records.
    """
    
    uri = "https://api.fantasydata.net/v3/nfl/stats/XML/FantasyDefenseBySeason/%s?key=%s" % (season, FANTASY_DATA_KEY)
    print uri
    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)


    wk = get_current_week().Week
    
    gs =Game.objects.filter(Week=wk)
    gsids = [g.id for g in gs] 
    root = ET.fromstring(resp.content)

    prs = root.findall('FantasyDefenseSeason')
    for p in prs:
        team = p.find('Team').text
        points = p.find('FantasyPointsFanDuel').text
        games    = p.find('Games').text
        print "{} {} {}".format(team, points, games)  
        avg = float(points)/int(games)
        tgs = TeamGame.objects.filter(team__abbr=team, game__in=gsids)
        for g in tgs:
            print "new avg {} for team game {}".format(avg, g)
            g.AverageFantasyPointsFanDuel = avg
            g.save()
