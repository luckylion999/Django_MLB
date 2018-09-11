
import xml.etree.cElementTree as ET
from django.test import TestCase
from app.models import *
from app.in_parse import *


class XpathTestCase(TestCase):
    
    def test_parse(self):
        f = 'data/xmlsep4/00minute-01hour.xml'
        root = ET.parse(f)
        
        boxscores = root.findall('BoxScore')
        for boxscore in boxscores:
            game = boxscore.findall('Game')
            if game:
                gamedata = elem_to_d(GameTags, game[0]) 
                #print "found Game data"
                #print gamedata
           
            playerreceiving = boxscore.findall('*/PlayerReceiving')
            print playerreceiving
            if playerreceiving:
                prdata = elem_to_d(PlayerReceivingTags, playerreceiving[0])
                print prdata 
            
            #print boxscore.findall('*/PlayerRushing')
            PlayerRushing = boxscore.findall('*/PlayerRushing')
            print PlayerRushing
            if PlayerRushing:
                prdata = elem_to_d(PlayerRushingTags, PlayerRushing[0])
                print prdata 
             
            PlayerPassing = boxscore.findall('*/PlayerPassing')
            print PlayerPassing
            if PlayerPassing:
                prdata = elem_to_d(PlayerPassingTags, PlayerPassing[0])
                print prdata 

            PlayerKickPuntReturns = boxscore.findall('*/PlayerKickPuntReturns')
            print PlayerKickPuntReturns
            if PlayerKickPuntReturns:
                prdata = elem_to_d(PlayerKickPuntReturnsTags, PlayerKickPuntReturns[0])
                print prdata 

            PlayerKicking = boxscore.findall('*/PlayerKicking')
            print PlayerKicking
            if PlayerKicking:
                prdata = elem_to_d(PlayerKickingTags, PlayerKicking[0])
                print prdata 

            # Look to game record to see which team is Away, which is Home
            AwayFantasyDefense = boxscore.findall('AwayFantasyDefense')
            print AwayFantasyDefense
            if AwayFantasyDefense:
                prdata = elem_to_d(FantasyDefenseTags, AwayFantasyDefense[0])
                print prdata 

            HomeFantasyDefense = boxscore.findall('HomeFantasyDefense')
            print HomeFantasyDefense
            if HomeFantasyDefense:
                prdata = elem_to_d(FantasyDefenseTags, HomeFantasyDefense[0])
                print prdata 