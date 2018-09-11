import xml.etree.cElementTree as ET
from paksite.settings import FANTASY_DATA_KEY
from app.models import *
import requests
from django.db import IntegrityError
from xml.dom import minidom
import pytz
import django
import json

TUESDAY = 1
#    Two-Point Conversions Scored (2PC/S)    2        TwoPointConversionReceptions, TwoPointConversionRuns
#    Two-Point Conversion Passes (2PC/P)    2        TwoPointConversionPasses
     
GameTags = ('GameKey', 'Week', 'Date', 'AwayTeam', 'HomeTeam', 'SeasonType', 'Season', 'Week', 'Stadium')
PlayerReceivingTags = ('PlayerID', 'Name', 'Team', 'Position', 'ReceivingYards', 'ReceivingTouchdowns', 'Receptions', 'FumblesLost', 'FumbleReturnTouchdowns', 'TwoPointConversionReceptions', 'TwoPointConversionRuns', 'TwoPointConversionReturns')
PlayerRushingTags = ('PlayerID', 'Name', 'Team', 'Position', 'RushingYards', 'RushingTouchdowns')
PlayerPassingTags = ('PlayerID', 'Name', 'Team', 'Position', 'PassingYards', 'PassingTouchdowns', 'PassingInterceptions')
PlayerKickPuntReturnsTags = ('PlayerID', 'Team', 'Position', 'PuntReturnTouchdowns', 'KickReturnTouchdowns')
PlayerKickingTags = ('PlayerID', 'Team', 'Position', 'FieldGoalsMade0to19', 'FieldGoalsMade20to29', 'FieldGoalsMade30to39', 'FieldGoalsMade40to49', 'FieldGoalsMade50Plus', 'ExtraPointsMade')
FantasyDefenseTags = ('GameKey', 'Team', 'Sacks', 'FumblesRecovered', 'InterceptionReturnTouchdowns', 'FumbleReturnTouchdowns', 'BlockedKickReturnTouchdowns',
                      'TwoPointConversionReturns', 'KickReturnTouchdowns', 'PuntReturnTouchdowns', 'Safeties', 'BlockedKicks', 'FantasyPointsFanDuel', 'FanDuelSalary')
APlayer = ('PlayerID', 'Name', 'Team', 'Position')
PlayerAllTags = set()
PlayerAllTags.update(PlayerReceivingTags)
PlayerAllTags.update(PlayerRushingTags)
PlayerAllTags.update(PlayerPassingTags)
PlayerAllTags.update(PlayerKickPuntReturnsTags)
PlayerAllTags.update(PlayerKickingTags)
PlayerAllTags.add('FantasyPointsFanDuel')
PlayerAllTags.add('FanDuelSalary')
PlayerAllTags.add('GameKey')

Teams = ('Key', 'TeamID', 'City', 'Name')

def update_all_attrs(obj, dic):
    for (key, value) in dic.items():
        if key == 'FanDuelSalary' and value == None:
            value = 4700
        try:
            setattr(obj, key, value)
        except Exception as e:
            print e 
    return obj
    
def elem_to_d(usetags, elem):
    gs = {}
    pdata = {}
    for e in elem.iter():
        if e.tag in ('GameKey', 'PlayerID', 'Name', 'Team', 'Position'):
            pdata[e.tag] = e.text
        elif e.tag in usetags:
            gs[e.tag] = e.text
            
            #if e.tag == 'FantasyPointsFanDuel':
            #    print pdata['GameKey']
            #    print Game.objects.get(GameKey=pdata['GameKey'])
            #    print 'FantasyPointsFanDuel: {}'.format(e.text)
            #    print '---'
    
    return gs, pdata
   
def add_or_get_player(pdata):
    # print pdata 
    if len(pdata):
        league, created = League.objects.get_or_create(name='NFL')
        team, created = Team.objects.get_or_create(abbr=pdata['Team'], league=league)
        try:
            player, created = Player.objects.get_or_create(PlayerID=pdata['PlayerID'], team=team)
        except IntegrityError as e:  # workaround for unique constraint when really seems it should just return it
            print team
            print pdata['PlayerID']
            created = False
            player = Player.objects.filter(PlayerID=pdata['PlayerID'], team=team)
            if len(player):
                player = player[0]
            else:
                print "failed to find this player"

        
        player.Name = pdata['Name']
        player.position = pdata['Position']
        player.save()
        
        return player
    
    return None



def update_offense(player, gameObj, prdata):     
    f = {'player_id': player.id, 'game_id': gameObj.id} 
    ofgame, created = PlayerGame.objects.get_or_create(**f)
    obj = PlayerGame.objects.get(id=ofgame.id)
    obj = update_all_attrs(obj, prdata)
    obj.save()

def update_player_data(Tags, playerdata, gameObj):
    prdata, pdata = elem_to_d(Tags, playerdata[0])
    player = add_or_get_player(pdata)
    update_offense(player, gameObj, prdata) 

# Defense 

def add_or_get_team(pdata):
    
    if len(pdata):
        league, created = League.objects.get_or_create(name='NFL')
        team, created = Team.objects.get_or_create(abbr=pdata['Team'], league=league)
        
        return team 
    return None

def update_defense_data(Tags, ddata, gameObj):
    prdata, pdata = elem_to_d(Tags, ddata)
    team = add_or_get_team(pdata)
    update_defense_rec(team, gameObj, prdata) 

def update_defense_rec(team, gameObj, prdata):     
    f = {'team_id': team.id, 'game_id': gameObj.id} 
    dgame, created = TeamGame.objects.get_or_create(**f)
    
    obj = TeamGame.objects.get(id=dgame.id)
    obj = update_all_attrs(obj, prdata)
    obj.save() 

def parse_teams(season):
    league, created = League.objects.get_or_create(name='NFL')

    uri = "https://api.fantasydata.net/v3/nfl/stats/JSON/Teams/%s?key=%s" % (season, FANTASY_DATA_KEY)

    resp = requests.get(uri)       

    if resp.status_code != 200:
        raise Exception(resp.status_code)

    teams = json.loads(resp.text)
    
    for team in teams:
        t, created = Team.objects.get_or_create(abbr=team['Key'], league=league)
        t.Name = team['Name']
        t.City = team['City']
        t.TeamID = team['TeamID']
        t.save()
        
def parse_defense(week, season=None):
    
    uri = "https://api.fantasydata.net/v3/nfl/stats/XML/FantasyDefenseByGame/%s/%s?key=%s" % (season, week, FANTASY_DATA_KEY)
    print uri
    resp = requests.get(uri)       
    
    if resp.status_code != 200:
        raise Exception(resp.status_code)

    print resp.text
    root = ET.fromstring(resp.text)
    dgames = root.findall('FantasyDefenseGame')
    for game in dgames:
        gk = game.findall('GameKey')
        print gk[0].text
        if gk:
            # creating game key but without details
            gameObj, created = Game.objects.get_or_create(GameKey=gk[0].text)
            print dgames
            update_defense_data(FantasyDefenseTags, game, gameObj)
            # print prdata 


def update_game_data(GameTags, game):
    gdata, pdata = elem_to_d(GameTags, game)
    if pdata.has_key('GameKey'):
        gameObj, created = Game.objects.get_or_create(GameKey=pdata['GameKey'])
        Game.objects.filter(id=gameObj.id).update(**gdata)
    
        return gameObj
    else:
        return None

def save_result(prefix, res, week, mins=3, season=2017, **kwargs):
    # data save case 
    if kwargs.has_key('save'):
        xml = minidom.parseString(res)  # or xml.dom.minidom.parseString(xml_string)
        items = xml.toprettyxml() 


        f = open('%s%s_%s_%s.xml' % (prefix, season, week, mins), 'w')
        f.write(str(items))
        f.close()        
           

def game_in_progress():
    uri = "https://api.fantasydata.net/v3/nfl/scores/xml/AreAnyGamesInProgress?key=%s" % FANTASY_DATA_KEY

    resp = requests.get(uri)       
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    
    in_progress = ET.fromstring(resp.text)

    if in_progress.text == "true":
        return True
    else:
        return False


def get_current_timeframe():
    myweek = Thisweek.objects.first()
    if not myweek:
        return get_timeframe()
    
    return Timeframe.objects.get(Week=myweek.Week, Season=myweek.Season, SeasonType=myweek.SeasonType)
    
        
def get_timeframe(type='current'):
    uri = "https://api.fantasydata.net/v3/nfl/stats/XML/Timeframes/%s?key=%s" % (type, FANTASY_DATA_KEY)
    resp = requests.get(uri)
    print resp.text
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    root = ET.fromstring(resp.text)
    tfs = root.findall('Timeframe')
    for tf in tfs:
        wk = (tf.find('Week').text or 0)
        if not wk:
            continue
        season = (tf.find('Season').text or 0)
        if int(season) < 2017:
            continue
        
        season_type = (tf.find('SeasonType').text or 0)
         
        tfobj, created = Timeframe.objects.get_or_create(
                                             SeasonType=tf.find('SeasonType').text,
                                             Season=tf.find('Season').text,
                                             Week=wk)
        if type == 'current':
            myweek = Thisweek.objects.first()
            if not myweek:
                myweek = Thisweek.objects.create()
            myweek.Week = wk
            myweek.Season = season
            myweek.SeasonType = season_type
            myweek.save()
                 
         
        for e in tf.iter():
            if e.tag in ('HasGames', 'HasStarted', 'HasEnded', 'HasFirstGameStarted', 'HasFirstGameEnded', 'HasLastGameEnded'):
                val = eval(e.text.title())
            else:
                val = e.text
            setattr(tfobj, e.tag, val)
            
        tfobj.save() 
    if type == 'current':
        return tfobj
    else:
        return "many timeframes loaded"

def get_current_week():

    now = timezone.now() 
    week = now.isocalendar()[1]
    last_game = GameMLB.objects.filter(Day__lte=now).last()
    
    return Thisweek.objects.first()
