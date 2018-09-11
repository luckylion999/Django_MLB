from django.template import loader, Context
from django.template.loader import get_template
from collections import OrderedDict
import traceback
from django.core.mail import send_mail
from paksite.settings import NO_EMAIL
import stripe
from app.models import ScheduleMLB 
import uuid 
from django.db.models import Max
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.db.models.query_utils import Q
import pytz

def get_next_or_current_game(team):
    
    # Find the next game (or current game) by team
    now = timezone.now().astimezone(pytz.timezone('US/Eastern'))
    
    game = ScheduleMLB.objects.filter(
        Q(HomeTeam=team) | Q(AwayTeam=team),
        Q(Status='InProgress') | Q(Status='Scheduled'),
        Season='2018',
        ).order_by('Day').first()
     
    return game


def send_my_mail(title, txt, email, html="", extra_recipient=None):

    print email
    if NO_EMAIL:
        print txt
    else:   
        sendto = [email,] 
        if extra_recipient:
            sendto.append(extra_recipient) 
        
        send_mail(title, txt, 'support-team@3pak.com',
              sendto, 
              fail_silently=False, html_message=html)

def week_placed(contest):

    # sorted and limited by number of payouts 
    return contest.sorted_by_position()

def calc_weekly_score(contest, week):
    print 'WEEKLY score for week {}'.format(week) 
    print contest
    tps = contest.threepaks.all() 
    for tp in tps:
        tp.final_week_1_score = tp.week_score(week)
        tp.save()
        print "{}:{}".format(tp.user.username, tp.final_week_1_score)
    
def calc_final_score_and_position(contest):

    # Per Bill's request, drop any of his or my users before calculating
    droppaks = contest.threepaks.filter(user__email__in=['devin@918.software', 'bill@3pak.com'])
    for drop in droppaks:
        print "Dropping threepak {}".format(drop)
        contest.threepaks.remove(drop)
     
    print '\n' 
    print contest
    tps = contest.threepaks.all() 
    for tp in tps:
        tp.final_points = tp.total_session_score()
        tp.save()
    
    tps = contest.threepaks.all()
    place = 1
    last_points = 0 
    for tp in tps:
        tp.final_place = place 
        if tp.final_points==last_points:
            tp.final_place = (place - 1)
        else:
            tp.final_place = place
            place +=1
            
        last_points = tp.final_points 
        tp.save()
        print "{} {} placed {}".format(tp.user.username, tp.final_points, tp.final_place)
    
    MIN_PLAYERS = 4
     
    # Hard coding prize calculations for existing customers for now
    # beer market co:  Top 10% - 1st, next 40% - 2nd, everyone else Free App 
    # flyting tee: 1st, 2nd, 3rd (no others)
    # pub fiction: Top 10% - 1st, next 40% - 2nd, everyone else Free App 
    tps = contest.threepaks.all()
    for tp in tps:
        if tp.user.usercompany.customer.name in ('dominos', 'flying-tee', 'expo', 'biggios', 'stoneys') or contest.num_players < MIN_PLAYERS:
            if tp.final_place==1:
                tp.prize_group=1
                tp.prize_text = tp.user.usercompany.customer.prize_label_1
                tp.prize_image = tp.user.usercompany.customer.prize_1
            if tp.final_place==2:
                tp.prize_group=2
                tp.prize_text = tp.user.usercompany.customer.prize_label_2
                tp.prize_image = tp.user.usercompany.customer.prize_2
            if tp.final_place==3:
                tp.prize_group=3
                tp.prize_text = tp.user.usercompany.customer.prize_label_3
                tp.prize_image = tp.user.usercompany.customer.prize_3
            
            if tp.prize_group>0:
                tp.prize_code = uuid.uuid4().hex[:6].upper()
                tp.save()
                print "{} prize group {} code {}, {}, {}".format(tp.user.username, tp.prize_group, tp.prize_code,
                                                                 tp.prize_text, tp.prize_image)
                    
        elif tp.user.usercompany.customer.name in ('beer-market-co', 'pub-fiction'):
            if tp.contest:
                 total = tp.contest.threepaks.aggregate(Max('final_place'))['final_place__max']
                 me    = tp.final_place
                 top10 = total * .10 # top 10%
                 top40 = total * .5 # next 40% 
                
                 # If less than 10 players, give first prize to 1st place user instead of to top 10% 
                 if top10 < 1 and me==1:
                     top10=1
                 
                 if me <= top10:
                    tp.prize_group=1
                    tp.prize_text = tp.user.usercompany.customer.prize_label_1
                    tp.prize_image = tp.user.usercompany.customer.prize_1
                 elif me <= top40:
                    tp.prize_group=2
                    tp.prize_text = tp.user.usercompany.customer.prize_label_2
                    tp.prize_image = tp.user.usercompany.customer.prize_2
                 else: 
                    tp.prize_group=3
                    tp.prize_text = tp.user.usercompany.customer.prize_label_3
                    tp.prize_image = tp.user.usercompany.customer.prize_3

            if tp.prize_group>0:
                tp.prize_code = uuid.uuid4().hex[:6].upper()
                tp.save()
                print "{} prize group {} code {}, {}, {}".format(tp.user.username, tp.prize_group, tp.prize_code,
                                                                 tp.prize_text, tp.prize_image)
        """
    #play_pos = calc_position(contest, user)
    if play_pos < 5.0:
        win = 1
        prize = customer.prize_label_1
        prize_img = customer.prize_1
    elif 15.0 > play_pos > 5.0:
        win = 2
        prize = customer.prize_label_2
        prize_img = customer.prize_2
    else:
        win = 3
        prize = customer.prize_label_3
        prize_img = customer.prize_3
 
    pak.prize_group = win
    pak.prize_code = uuid.uuid4().hex[:6].upper()
    pak.save()
        """
        
def make_payments(week=None):
    return None  #reveiw

    # week is start week
    
    #for testing
    #stripe.api_key = STRIPE_TEST_SECRET
   
    # Note run Tuesday
      
    if week==None: 
        tf = Thisweek.objects.last()
    else:
        tf = Timeframe.objects.get(Week=week, Season=2015)
       
    print "Payout processing for 3pak session weeks {}-{}".format(tf.Week, tf.Week+1) 
    print "----------------------------------------------\n\n"    
    try:
        contests = Contest.objects.filter(threepaks__start_week=tf.Week, threepaks__final_win__gt=0).distinct()

        for contest in contests:
            numpays = TournamentPlacement.objects.filter(spec=contest.spec).count() 
            calc_payout(contest) #removed
            print "---\nContest {}\n---".format(contest.id)
            # payments already calculated 
            wins = contest.threepaks.filter(final_win__gt=0).order_by('final_place')[:numpays]

            for win in wins:
                print "Place {}: \n{} wins: {}".format(win.final_place, win.user.username, win.final_win)
                try:
                    tk = StripeToken.objects.get(user=win.user)
                    #print "recipient token:{}".format(tk.recipient_id)
                   
                    if len(tk.recipient_id):
                        
                        # Get first card on the customer account
                        rs = stripe.Recipient.retrieve(tk.recipient_id)
                        cardid = rs.cards.data[0].id
 
                        # Create a transfer to the specified recipient
                        transfer = stripe.Transfer.create(
                          amount = int(win.final_win * 100), # amount in cents
                          currency = "usd",
                          recipient = tk.recipient_id,
                          card = cardid,
                          statement_descriptor = "3pak"
                        )
                        
                        print "transfer initiated for {}.  Transfer id: {}".format(tk.user.username, transfer.id)
                    else:
                        print "Insufficient recipient information collected.  Must manually pay." 
                except Exception as ex:
                    print "Insufficient recipient information collected.  Must manually pay." 
           
                #c =stripe.Customer.create(description=tk.user.email, source=tk.token)
                #logger.debug("able to create stripe customer")
                #cus_7N0TL6Ob2FqVz9
    except Exception as ex:
        print ex.message

def test_end_of_week():
  
    myweek = Thisweek.objects.last().Week  
    
    game_over_paks = ThreePak.objects.filter(start_week=myweek-1)
    ongoing_paks = ThreePak.objects.filter(start_week=myweek)
 
     
    over_contests = Contest.objects.filter(threepaks__in=game_over_paks).distinct()
    for c in over_contests:
        print c
        #calc_final_score_and_position(c)

    for pak in game_over_paks:
        try:
            contest = Contest.objects.get(threepaks=pak.id)
            
            user = pak.user
            customer = UserCompany.objects.get(user=user).customer
            
           
            # Hard coding prize calculations for existing customers for now
            # beer market co:  Top 10% - 1st, next 40% - 2nd, everyone else Free App 
            # flyting tee: 1st, 2nd, 3rd (no others)
            # pub fiction: Top 10% - 1st, next 40% - 2nd, everyone else Free App 
            
            #play_pos = calc_position(contest, user)
        except Exception as ex:
            print ex
           

def end_of_week1(): 
    # This logic is valid as long as this function is called Wednesday morning 
    now_week, last_week, start_week = Timeframe.get_previous_timeframes()
    ongoing_paks = ThreePak.objects.filter(
        start_week=last_week.Week,
        season=last_week.Season,
        season_type=last_week.SeasonType
    )

    ongoing_contests = Contest.objects.filter(threepaks__in=ongoing_paks).distinct()
    for c in ongoing_contests:
        calc_weekly_score(c, last_week.Week)
        try:
            contest_paks = c.threepaks.all().order_by('-final_week_1_score')


            for pak in contest_paks:
                title = "3pak Weeks {} results".format(pak.session_weeks_str)
               
                this_week = last_week.Week 
                
                t2 = get_template('week_one_over.html')
                htmltxt = t2.render(locals())

                for p in contest_paks: 
                    print p.user.username
                    print p.final_week_1_score


                send_my_mail(title, "",  pak.user.email, html=htmltxt)
                #send_my_mail(title, "",  'devin@918.software', html=htmltxt)
            
        except Exception as ex:
            print ex.message
            traceback.print_stack()
           
            
def end_of_session():
 
    # This logic is valid as long as this function is called Wednesday morning 
    now_week, last_week, start_week = Timeframe.get_previous_timeframes()
    game_over_paks = ThreePak.objects.filter(
        start_week=start_week.Week,
        season=start_week.Season,
        season_type=start_week.SeasonType
    )

    over_contests = Contest.objects.filter(threepaks__in=game_over_paks).distinct()
    for c in over_contests:
        calc_final_score_and_position(c)
        try:
            contest_paks = c.threepaks.all()

            for pak in contest_paks:
                title = "3pak session is a wrap. Did you win?"
                t2 = get_template('session_over_new.html')
                htmltxt = t2.render(locals())

                for p in contest_paks:
                    print "{}, {}, {}, {}".format(p.user.username, p.final_points, p.final_place, p.prize_text)
                
                extra_recipient = None 
                if c.customer.name=='stoneys': 
                    extra_recipient = 'will@stoneysbarandgrill.com'
                    
                send_my_mail(title, "",  pak.user.email, html=htmltxt, extra_recipient=extra_recipient)
                #send_my_mail(title, "",  'devin@918.software', html=htmltxt)
                # Send to will@stoneysbarandgrill.com for Stoney's  - per request on Aug 31, 2017
                    
        except Exception as ex:
            print ex.message



