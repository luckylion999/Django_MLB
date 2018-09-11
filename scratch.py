#export DJANGO_SETTINGS_MODULE=paksite.settings

import django
django.setup()

from django.contrib.auth.models import User, Group
from app.in_parse import get_current_week, get_timeframe
from app.models import *
import random
from app.fetch.player_data import *
from app.payout import *
from app.payment import *
from app.views import *

#from push_notifications.models import APNSDevice
#dev = APNSDevice.objects.first()
#dev.send_message("testing push")

"""
from django.test.client import RequestFactory

for i in range(127,237):
   
    u = User.objects.create(username="BETA{}".format(i)) 
    tp = ThreePak.objects.create(start_week=12, user=u)
    
    factory = RequestFactory()
    request = factory.get('/start_contest/?3pak=%d' % tp.id )
    request.user = u
    response = start_contest(request)
    print response
# calculate placement and lookup payout
contest = Contest.objects.filter(start_week=10).first()
calc_payout(contest)

winners = contest.threepaks.filter(final_win__gt=0).order_by('final_place')

title = "3pak session is a wrap. How did you do?"  
c = Context(locals())
t = get_template('session_over.txt')
txt = t.render(c)
print txt


t2 = get_template('session_over.html')
htmltxt = t2.render(c)
print htmltxt
#sunday_games_started()
#end_of_week()
"""
# calculate placement and lookup payout

#make_payments(10)

"""
d = Game.objects.filter(Date__year=2015)
print d
from datetime import datetime
import pytz
SUNDAY=6
now = timezone.localtime(timezone.now())

days_ahead = SUNDAY - now.weekday()
if days_ahead <= 0: # Target day already happened this week
    days_ahead += 7
sunday = now + timedelta(days_ahead)

and scratch 1

week = get_current_week()
myuser = User.objects.last()

ThreePak.objects.all().delete()
pak, created = ThreePak.objects.get_or_create(user=myuser, start_week=week)
print pak
pidx = int(random.random() * PlayerGame.objects.filter(game__Week=week, FanDuelSalary__gt=0).count())
pidx2 = int(random.random() * PlayerGame.objects.filter(game__Week=week, FanDuelSalary__gt=0).count())
pidx3 = int(random.random() * TeamGame.objects.filter(game__Week=week, FanDuelSalary__gt=0).count())
p1 = PlayerGame.objects.filter(game__Week=week,FanDuelSalary__gt=0)[pidx] 
p2 = PlayerGame.objects.filter(game__Week=week,FanDuelSalary__gt=0)[pidx2] 
p3 = TeamGame.objects.filter(game__Week=week,FanDuelSalary__gt=0)[pidx3] 
print p1
print p2
print p3
print pak.make_pick(p1) 
print pak.make_pick(p2) 
print pak.make_pick(p3) 

scratch 2
myuser = User.objects.first()
pak, created = ThreePak.objects.get_or_create(user=myuser, start_week=week)
print pak
topsal = PlayerGame.objects.filter(game__Week=week,FanDuelSalary__gt=0).order_by('-FanDuelSalary') 
print pak.make_pick(topsal[0]) 
print pak.make_pick(topsal[1]) 
print pak.make_pick(topsal[2]) 

scratch 3
pak = ThreePak.objects.last()
contests = Contest.objects.filter(threepaks=pak.id)

# calculate placement and lookup payout
if len(contests):
    contest = contests.first()
    ss = contest.sorted_by_position() # remember zero based

    payoutstr = ""
        
    # we need the lessor of max_players and actual players
    idxtotal = contest.spec.max_players
    if contest.threepaks.count() < contest.spec.max_players:
        idxtotal = contest.threepaks.count()
    
    for i in range(0, idxtotal):
        print i
        apak = ss[i]
        apak.final_place= i+1
        apak.final_win  = get_payout(contest, apak.final_place)
        apak.ended = True
        apak.save()   
        payoutstr += "%s is in position %d and wins $%s\n" % (apak.user.username, apak.final_place,
                                                                     apak.final_win)
        
title = "%s is over." % tf 
c = Context(locals())
t = get_template('week_over.txt')
txt = t.render(c)
print txt

# another scratch
week = get_current_week()
pak, created = ThreePak.objects.get_or_create(user__username='devin@gitwitcreative.com', start_week=week)
print pak.id
print created
ts = TournamentSpec.objects.get(tourny_type=TournamentSpec.THREE_4_THIRTY)
contest = Contest.objects.enter_contest(ts, pak)
print ts
print contest
"""