from django.core.management.base import BaseCommand
from django.db.models import Q
import os
import requests
from app.parse import *
from app.models import *
import time
import random

def fake_game_in_progress():
    #maybe get fancy and only return True if timeframe of this week overlaps 2015 game times
    return True

def zero_score(obj):
    obj.FantasyPointsFanDuel = 0 
    obj.save()

def increment_score(obj):
    print "incrementing score"
    final = obj.DemoFantasyPointsFanDuel
    old = obj.FantasyPointsFanDuel
    r = random.randrange(0,10)
    m = r * 0.1
    if r <7:
    	new = old + 7 
    else: 
    	new = old + 3 
    if new < final:
        print "From {} to {} toward {}".format(old, new, final)
        obj.FantasyPointsFanDuel = new
        obj.save()
    else:
        print "exceeded final score so saving final to destination"
        obj.FantasyPointsFanDuel = obj.DemoFantasyPointsFanDuel
        obj.save()


def get_fake_current_week():
    # While in DEMO mode, always return week 13, 14
    week = Thisweek.objects.last() 

    # Just getting week of year.  If even, calling it week 13, if odd, calling it 16 
    week_of_year = django.utils.timezone.now().isocalendar()[1]
    if (week_of_year % 2 == 0): #Even
        week.Week=14 
    else:
        week.Week=13 
    week.save()
    return week
         
class Command(BaseCommand):

    def handle(self, *args, **options):

#TODO, bring a fresh database over from prod, review logic and continue to test
# TODO set up DemoFantasyPoints before running this command

        # refresh model
        week = get_fake_current_week() 
        print "current DEMO week: {}".format(week.Week)

        # zero simulation
        games =  PlayerGame.objects.filter(
           game__Week=week.Week,
           game__Season=week.Season,
           game__SeasonType=week.SeasonType,
           DemoFantasyPointsFanDuel__gt=0
        )
        print "found {} games".format(games.count()) 
        if not len(games):
            # First run...copy FantasyPointsFanDuel to DemoFPFD for refererence
            games =  PlayerGame.objects.filter(
               game__Week=week.Week,
               game__Season=week.Season,
               game__SeasonType=week.SeasonType,
               DemoFantasyPointsFanDuel=0
            )
            print "found games in week {}".format(len(games))
            for g in games:
               g.DemoFantasyPointsFanDuel = g.FantasyPointsFanDuel
               g.save()
            print "Saved first run games"
        
        for obj in games:
            zero_score(obj)
            
        games =  TeamGame.objects.filter(
           game__Week=week.Week,
           game__Season=week.Season,
           game__SeasonType=week.SeasonType,
           DemoFantasyPointsFanDuel__gt=0
        )
        if not len(games):
            # First run...copy FantasyPointsFanDuel to DemoFPFD for refererence
            games =  TeamGame.objects.filter(
               game__Week=week.Week,
               game__Season=week.Season,
               game__SeasonType=week.SeasonType,
               DemoFantasyPointsFanDuel=0
            )
            for g in games:
               g.DemoFantasyPointsFanDuel = g.FantasyPointsFanDuel
               g.save()
            print "Saved first run TEAM games"
        for obj in games:
            zero_score(obj)
           
      
        # DEMO mode: is always week 15 or 16, so clear any ThreePaks
        if week.Week==13:
            print "Week 13 cleanup"
            paks = ThreePak.objects.filter(Q(start_week=13) | Q(start_week=14))
        else:
            print "Week 14, so no cleanup"
      	    return
 
        for p in paks:
            # Remove all picks
            p.pick_set.clear()
            # Remove final scores from 3pak
            p.final_points=0
            p.final_place=0
            p.final_win=0
            p.save()
      
        # Loop runs for one week (168/7 = 24 hours)  
        for i in range(1,168): 
            if fake_game_in_progress():
                print "iteration: {}".format(i)
           	print "week: {}".format(week.Week) 
           	print "season: {}".format(week.Season) 
           	print "season type: {}".format(week.SeasonType) 
                games =  PlayerGame.objects.filter(
                   game__Week=week.Week,
                   game__Season=week.Season,
                   game__SeasonType=week.SeasonType,
                   DemoFantasyPointsFanDuel__gt=0
                )
		print games

                for obj in games:
                    increment_score(obj)
                    
                games =  TeamGame.objects.filter(
                    game__Week=week.Week,
                    game__Season=week.Season,
                    game__SeasonType=week.SeasonType,
                    DemoFantasyPointsFanDuel__gt=0
                )
		print games
                for obj in games:
                    increment_score(obj)
		print 'end of iteration'
            else:
                print "no fake game in progress"     
            # maybe sleep 1 hour when ready        
            time.sleep(60*60)
        
