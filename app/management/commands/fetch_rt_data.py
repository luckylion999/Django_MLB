from django.core.management.base import BaseCommand
import xml.etree.cElementTree as ET
from paksite.settings import FANTASY_DATA_KEY
import os
import requests
from app.parse import *
import time
from app.fetch.fantasy_players import get_fantasy_players
from app.fetch.player_data import get_player_data
from django.core.mail import send_mail
import os, psutil
 
class Command(BaseCommand):

    def handle(self, *args, **options):

        my_pid = os.getpid()                      
        print "my pid is {}".format(my_pid) 
        pids = psutil.pids()  # get list of active pids

        for pid in pids:
            if pid != my_pid:
                try:
                    p = psutil.Process(pid)
                    cmdstr = ' '.join(p.cmdline()) 
                    print cmdstr
                    if cmdstr.find('fetch_rt_data') > -1:
                        p.kill()
                        print "killed process: {}".format(pid)
                        time.sleep(10)
                # if we can't access command info skip it
                except psutil.AccessDenied:
                    None
                                                                            
                     

        gamestarted = False
        while True:
            time.sleep(10)
            try:
                tf = get_current_timeframe()
                print "{} {} {}".format(tf.Season, tf.SeasonType, tf.Week)

                print "Game in progress...?"
                if game_in_progress():
                    if not gamestarted:
                        # Let's just do this once per each new game time...
                        parse_teams(tf.Season)
                        get_fantasy_players()
                        
                        #send_mail('fetch_rt_data.py', 'game in progress...', 'no-reply@3pak-testing.com',
                        #  ['devin@918.software',], 
                        #  fail_silently=False )
                        
                        gamestarted=True
                    
                    print "game on..."

                    week = get_current_week().Week

                    for i in range(50):
                        print "looping 50 per implementation guide advice"
                        get_player_data(week, season=tf.season_str)
                        parse_defense(week, season=tf.season_str)
                        time.sleep(2)
                time.sleep(10)
                gamestarted = False
            except Exception, e:
                print('Exception Raised in fetch_rt_data. Error Code: {0}'.format(e))
