import random
import stripe
import decimal

from shapely.geometry import Point as shapelyPoint
from shapely.geometry.polygon import Polygon
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.permissions import AllowAny
import logging
from app.models import (
    TeamMLB, 
    StadiumMLB, 
    GameMLB, 
    PlayerMLB
    )
from app.serializers import *
from django.utils import timezone
from app.parse import get_current_week, get_current_timeframe
from app.util import get_next_or_current_game
logger = logging.getLogger(__name__)


def promo_range(now):
    specialstart = now.replace(
        year=2015,
        month=12,
        day=23,
        hour=8,
        minute=0,
        second=0)
    specialend = now.replace(
        year=2015,
        month=12,
        day=27,
        hour=13,
        minute=0,
        second=0)
    return specialstart, specialend


class BigResultsPagination(PageNumberPagination):
    page_size = 2000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class TeamMLBViewSet(viewsets.ModelViewSet):
    queryset = TeamMLB.objects.all()
    serializer_class = TeamMLBSerializer


class StadiumMLBViewSet(viewsets.ModelViewSet):
    queryset = StadiumMLB.objects.all()
    serializer_class = StadiumMLBSerializer


class GameMLBViewSet(viewsets.ModelViewSet):
    queryset = GameMLB.objects.all()
    serializer_class = GameMLBSerializer


class PlayerMLBViewSet(viewsets.ModelViewSet):
    queryset = PlayerMLB.objects.all()
    serializer_class = PlayerMLBSerializer

 
class PlayerGameMLBViewSet(viewsets.ModelViewSet):    
    serializer_class = PlayerGameMLBSerializer
    pagination_class = BigResultsPagination

    def get_queryset(self):
        team = self.request.user.profile.customer
        return common_player_queryset(team, PlayerGameMLB)

class TeamGameMLBViewSet(viewsets.ModelViewSet):
    queryset = TeamGameMLB.objects.all()
    serializer_class = TeamGameMLBSerializer


class PlayerSeasonMLBViewSet(viewsets.ModelViewSet):
    queryset = PlayerSeasonMLB.objects.all()
    serializer_class = PlayerSeasonMLBSerializer


class TeamSeasonMLBViewSet(viewsets.ModelViewSet):
    queryset = TeamSeasonMLB.objects.all()
    serializer_class = TeamSeasonMLBSerializer


class NewsMLBViewSet(viewsets.ModelViewSet):
    queryset = NewsMLB.objects.all()
    serializer_class = NewsMLBSerializer


def common_player_queryset(team, object):

    schedule = get_next_or_current_game(team) 
   
    if schedule: 
        player_game = object.objects.filter(
            GameID=schedule.GameID,
        )
        if schedule.HomeTeam == team.name:
            player_game = player_game.filter(HomeOrAway='HOME')
        else:
            player_game = player_game.exclude(HomeOrAway='HOME')
            
        return player_game
    return []

class PlayerGameProjectionMLBViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerGameProjectionMLBSerializer
    pagination_class = None
    
    def get_queryset(self):

        team = self.request.user.profile.customer
        return common_player_queryset(team, PlayerGameProjectionMLB)

class PlayerSeasonProjectionMLBViewSet(viewsets.ModelViewSet):
    queryset = StandingMLB.objects.all()
    serializer_class = StandingMLBSerializer


class StandingMLBViewSet(viewsets.ModelViewSet):
    queryset = StandingMLB.objects.all()
    serializer_class = StandingMLBSerializer


class DfsSlatePlayerMLBViewSet(viewsets.ModelViewSet):
    queryset = DfsSlatePlayerMLB.objects.all()
    serializer_class = DfsSlatePlayerMLBSerializer


class DfsSlateGameMLBViewSet(viewsets.ModelViewSet):
    queryset = DfsSlateGameMLB.objects.all()
    serializer_class = DfsSlateGameMLBSerializer


class DfsSlateMLBViewSet(viewsets.ModelViewSet):
    queryset = DfsSlateMLB.objects.all()
    serializer_class = DfsSlateMLBSerializer


class InningMLBViewSet(viewsets.ModelViewSet):
    queryset = InningMLB.objects.all()
    serializer_class = InningMLBSerializer


class BoxScoreMLBViewSet(viewsets.ModelViewSet):
    queryset = BoxScoreMLB.objects.all()
    serializer_class = BoxScoreMLBSerializer


class ScheduleMLBViewSet(viewsets.ModelViewSet):
    queryset = ScheduleMLB.objects.all()
    serializer_class = ScheduleMLBSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permissions_classes = [AllowAny, ]
    lookup_field = 'name'


class TournamentSpecViewSet(viewsets.ModelViewSet):
    queryset = TournamentSpec.objects.all().order_by('-guaranteed_payout')
    serializer_class = TournamentSpecSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-Updated')
    serializer_class = NewsSerializer


class TournamentPlacementViewSet(viewsets.ModelViewSet):
    queryset = TournamentPlacement.objects.all()
    serializer_class = TournamentPlacementSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        customer = CustomerProfile.objects.get(
            name=request.data.get('customer'))
        user_profile = obj.profile
        user_profile.customer = customer
        user_profile.save()
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=obj)
        response = serializer.data
        response.update({'AUTHTOKEN': token.key})
        return Response(
            response,
            status=status.HTTP_201_CREATED,
            headers=headers)


def secs_to_hours(secs):
    return (secs / 60) / 60



def salaries_are_available():

    # Only convert to Eastern when checking day of week
    now = timezone.now().astimezone(pytz.timezone('US/Eastern'))

    if now.weekday() in (DayOfWeek.MONDAY, DayOfWeek.TUESDAY):
        return False

    return True


@api_view(['POST', 'GET'])
def set_card_name(request):
    try:
        first = request.GET.get('first_name', None)
        last = request.GET.get('last_name', None)
        request.user.first_name = first
        request.user.last_name = last
        request.user.save()
        return JsonResponse({'saved': True})
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})


def get_payouts(request):
    try:
        ret = {}
        tsid = request.GET.get('tournament_spec_id', None)
        return JsonResponse(ret)
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)


def window_info(request):

    # display results in central time
    timezone.activate(pytz.timezone("US/Central"))
    tf = get_current_timeframe()

    info = {}
    info['Salaries are available'] = salaries_are_available()

    # Only convert to Eastern when checking day of week
    weekday_now = timezone.now().astimezone(pytz.timezone('US/Eastern'))

    now = timezone.now()

    if DayOfWeek.WEDNESDAY != weekday_now.weekday():
        wed = next_weekday(weekday_now, DayOfWeek.WEDNESDAY)
    else:
        wed = now
    wed = wed.replace(hour=0, minute=0, second=0, microsecond=0)
    info['Next Wednesday'] = wed
    info['Next Wednesday (minutes until)'] = round(
        (wed - now).total_seconds() / 60)

    cweek = get_current_week()

    seasontype = Thisweek.objects.first().SeasonType
    pgs = PlayerGame.objects.filter(
        game__Date__gte=now,
        FanDuelSalary__gt=0).exclude(
        player__CurrentStatus__in=(
            "Suspended",
            "Out")).order_by('game__Date')
    if pgs.count():
        next = pgs.first()
        info['Next game'] = next.game.vs
        info['Next game time'] = next.game.Date
        info['GameKey'] = next.game.GameKey
        info['Pick selection locked for {}'.format(
            info['Next game'])] = locked(next.game)
        info['Minutes until next game'] = round(
            (next.game.Date - now).total_seconds() / 60)
        info['Hours until next game'] = round(
            (next.game.Date - now).total_seconds() / 60 / 60, 1)
        info['Minutes until next player unselectable'] = round(
            (lock_at(next.game) - now).total_seconds() / 60)

    if DayOfWeek.SUNDAY == weekday_now.weekday():
        wclose = now.replace(hour=19, minute=30, second=0, microsecond=0)
        info['Last sunday game started'] = sunday_games_started()
        info['Window closes (minutes)'] = round(
            (wclose - now).total_seconds() / 60)

    last_updated = PlayerGame.objects.filter(
        FantasyPointsFanDuel__gt=0).order_by('-updated')[:3]

    return render(request, 'info.html', context=locals())


def leaderboard(request, customer):

    profile = CustomerProfile.objects.get(name=customer)

    ads = []
    if profile.page_ad:
        ads.append(profile.page_ad.url)
    if profile.page_ad_2:
        ads.append(profile.page_ad_2.url)
    if profile.page_ad_3:
        ads.append(profile.page_ad_3.url)
    if profile.page_ad_4:
        ads.append(profile.page_ad_4.url)

    total_ads = len(ads)
    if total_ads:
        ad_seq = request.session.get('ad_seq', 0)
        if ad_seq > total_ads:
            ad_seq = total_ads - 1
        try:
            page_ad_url = ads[ad_seq]

            ad_seq += 1
            if ad_seq >= total_ads:
                ad_seq = 0
            request.session['ad_seq'] = ad_seq
        except BaseException:
            page_ad_url = ''
            request.session['ad_seq'] = 0

    week = get_current_week()

    tm_now = Timeframe.objects.get(
        Season=week.Season,
        SeasonType=week.SeasonType,
        Week=week.Week)
    tms = [tm_now, ]

    has_contest = Contest.objects.filter(
        customer=profile,
        start_week=tm_now.Week,
        season_type=tm_now.SeasonType,
        season=tm_now.Season
    ).count()

    last_session = request.session.get('last_session', False)
    if last_session or not has_contest:
        try:
            tms.insert(
                0, Timeframe.objects.filter(
                    StartDate__lt=tm_now.StartDate).latest('StartDate'))
        except Exception as e:
            None
        # No prior timeframes...will default to showing the same
        try:
            del request.session['last_session']
        except BaseException:
            None
    else:
        request.session['last_session'] = True

    contest = None
    for tm in tms:
        contests = Contest.objects.filter(
            customer=profile,
            start_week=tm.Week,
            season_type=tm.SeasonType,
            season=tm.Season
        )
        if len(contests):
            contest = contests[0]
            break

    # return JsonResponse(tms, safe=False)
    if contest:
        top_players = contest.get_positions()
        top_five = top_players[:5]
        top_to_ten = top_players[5:10]
    # else:
    #    return JsonResponse(tms, safe=False)

    news = ""
    recent_news = list(News.objects.all().order_by('-Updated')[:4])
    random.shuffle(recent_news)
    for n in recent_news:
        news += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class='less'>{}</span>".format(
            n.Title.encode('utf-8'), n.Content.encode('utf-8'))

    return render(request, 'index.html', context=locals())


@api_view(['GET', 'POST'])
def pick_window_open(request):
    
    return JsonResponse({'window_is_open': True, 'demo_mode': True})

    """
    Notes:
    
    team = request.user.profile.customer
    schedule = get_next_or_current_game(team) 

    # remove after testing
    today = timezone.localtime() 
    tomorrow = timezone.localtime() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0) 
    mins_until_open = round((tomorrow - today).total_seconds() / 60)
    return JsonResponse({'window_is_open': False,
                         'mins_until_open': mins_until_open,
                         'demo_mode': False})
    # remove after testing

    # If game is scheduled today, only allow player changes until top of fourth inning
    if schedule:
        inning = InningMLB.objects.filter(GameID=schedule.GameID).first()

        if inning and inning.InningNumber >= OPEN_PICK_INNING_CUTOFF:

            today = timezone.localtime() 
            tomorrow = timezone.localtime().date() + timedelta(days=1)

            mins_until_open = round((tomorrow - today).total_seconds() / 60)
            return JsonResponse({'window_is_open': False,
                                 'mins_until_open': mins_until_open,
                                 'demo_mode': False})
            return JsonResponse({'window_is_open': False, 'demo_mode': True})
        else:  
            return JsonResponse({'window_is_open': True, 'demo_mode': True})
         
    
    return JsonResponse({'window_is_open': True, 'demo_mode': True})
    
    
    tf = get_current_timeframe()

    # Bill instructed us to end season early: no new sessions starting with
    # week 16 or greater
    if tf.Week > 15:
        return JsonResponse({'window_is_open': False, 'demo_mode': True})

    if tf.HasStarted and salaries_are_available() and sunday_games_started() == False:
        return JsonResponse({'window_is_open': True, 'demo_mode': True})
    else:

        now = timezone.localtime(timezone.now())

        # Only convert to Eastern when checking day of week
        weekday_now = timezone.now().replace(tzinfo=pytz.timezone('US/Eastern'))

        if DayOfWeek.WEDNESDAY != weekday_now.weekday():
            wed = next_weekday(now, DayOfWeek.WEDNESDAY)
        else:
            wed = now
        wed = wed.replace(hour=0, minute=0, second=0, microsecond=0)

        mins_until_open = round((wed - now).total_seconds() / 60)
        return JsonResponse({'window_is_open': False,
                             'mins_until_open': mins_until_open,
                             'wednesday': wed,
                             'demo_mode': False})
    """


def format_date(date):
    m = date.strftime('%B')
    d = date.strftime('%-d')
    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][date.day % 10 - 1]
    return "{} {}{}".format(m, d, suffix)


def get_current_week_api(request):
    tw = Thisweek.objects.first()
    week = tw.Week

    now = timezone.localtime(timezone.now())

    start = None
    end = None

    # session start week
    try:
        tf1 = Timeframe.objects.get(
            Week=week,
            Season=tw.Season,
            SeasonType=tw.SeasonType)
        start = tf1.StartDate
    except Exception as ex:
        return JsonResponse({'error': ex.message, 'error_code': ex.err_code()})

    # session end week
    try:
        tf2 = Timeframe.objects.get(
            Week=week + 1,
            Season=tw.Season,
            SeasonType=tw.SeasonType)
        end = tf2.EndDate
    except Exception as ex:
        # Use end of tf1
        end = start + timedelta(days=7)

    # Bill prefers we use day of first game for start day, and day of last
    # game for end day, so adjust
    start = start + timedelta(days=1)
    end = end - timedelta(days=1)

    res = {'week': week,
           'start_day': format_date(start),
           'end_day': format_date(end)}
    return JsonResponse(res)


@api_view(['GET', 'POST'])
def dashboard(request):
    try:
        res = {}

        if request.method == 'GET':
            pakid = request.GET.get('3pak', None)
        else:
            pakid = request.POST.get('3pak', None)

        if pakid is None:
            # To be more fault resiliant, if 3pak is missing, try to pull
            # one for the user in the current session.  This rule may not
            # be valid in future releases, so review.
            # week = get_current_week().Week
            now = timezone.localtime(timezone.now())

            # packs = ThreePak.objects.filter(Q(start_week=week) | Q(
            #     start_week=week - 1), user=request.user)
            packs = ThreePak.objects.filter(user=request.user)
            if len(packs):
                pakid = packs.last().id

        mypak = ThreePak.objects.get(id=pakid)
        
        res['my_score'] = mypak.total_session_score()
        # res['session_over'] = mypak.is_session_over()
        res['pick_details'] = []
        picks = mypak.pick_set.all()
        
        for p in picks:
            details = {}
            details['score'] = p.score()
            details['name'] = p.content_object.get_name()
            details['player_team_id'] = p.content_object.get_entity_id()
            details['id'] = p.content_object.PlayerID
            details['vs'] = p.content_object.vs

            res['pick_details'].append(details)

        
        try:
            contest = Contest.objects.get(threepaks__id=pakid)
        except BaseException:
            res['positions'] = []
            return JsonResponse(res)

        res['positions'] = contest.get_positions()
        
        return JsonResponse(res)
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})


@api_view(['GET', ])
def is_stripe_registered(request):
    try:
        tk = StripeToken.objects.filter(user=request.user).last()
    except Exception as ex:
        return JsonResponse({'error': ex.message})

    if tk:
        return JsonResponse({'registered': (len(tk.customer_id) > 1)})
    else:
        return JsonResponse({'registered': False})


@api_view(['GET', ])
def payment_received(request):
    try:
        tk = StripeToken.objects.filter(user=request.user).last()
        pakid = get_pakid(request)
        ch = StripeCharge.objects.filter(threepak__id=pakid)
    except Exception as ex:
        return JsonResponse({'error': ex.message})

    try:
        return JsonResponse({'payment_received': ch.first().charge_id})
    except Exception as ex:
        # allow for DEMO
        return JsonResponse({'payment_received': 0})


def calc_charge(request):
    try:
        specids = request.GET.getlist('spec_ids')
        cost = TournamentSpec.objects.filter(
            id__in=specids).aggregate(
            Sum('cost'))['cost__sum']
        return "{}00".format(cost)
    except BaseException:
        # historically was always $3
        return 300

        # historically was always $3
    return 300


@api_view(['POST', 'GET'])
def register_stripe_token(request):
    try:
        token = request.GET.get('stripe_token', None)
        token2 = request.GET.get('stripe_token2', None)

        if token:
            # Log for our purposes
            tk = StripeToken.objects.create(token=token, user=request.user)

            # fetch or create customer object in stripe
            r = ""
            c = None
            try:
                c = stripe.Customer.create(
                    description=tk.user.email, source=tk.token)
                logger.debug("able to create stripe customer")
            except Exception as err:
                r = "er1: {}".format(err.message)
                logger.debug("Exception")
                logger.debug(err.message)

            if not c:
                raise Exception(r)

            tk.customer_id = c.id
            tk.save()
            logger.debug("saved our record")

            amount = calc_charge(request)
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                customer=tk.customer_id,
                description="3pak"
            )
            logger.debug("seems like we charged")

            # Track the charge in our DB
            StripeCharge.objects.create(
                token=tk, threepak=ThreePak.objects.get(
                    id=get_pakid(request)), charge_id=charge.id)

            # New:  if we have 2nd stripe token, we create recipient
            if token2:
                try:
                    try:
                        name = "{}".format(request.user.first_name)
                        email = request.user.email
                    except BaseException:
                        name = "Name Unknown"
                        email = "unknown@unknown.com"
                    rec = stripe.Recipient.create(
                        name=name,
                        type="individual",
                        email=email,
                        card=token2)
                    tk.recipient_id = rec.id
                    tk.save()
                except Exception as err:
                    r = "{}, er3: {}".format(err, err.message)
                    logger.debug("Exception in create recipient")
                    logger.debug(err)

            return JsonResponse({'card_ready': True})
        else:
            raise Exception("No token provided")
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})


@api_view(['POST', 'GET'])
def start_contest(request):
    try:
        pakid = request.GET.get('3pak', None)

        now = timezone.localtime(timezone.now())

        contest = Contest.objects.enter_contest(
            None, ThreePak.objects.get(id=pakid)
        )
        cids = []
        cids.append(contest.id)

        if len(cids) == 1:
            return JsonResponse({'success': True, 'contest_id': cids[0]})
        else:
            return JsonResponse({'success': True, 'contest_ids': cids})

    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})

# for debugging purpose only...
def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )


def get_pakid(request):
    pakid = request.GET.get('3pak', None)
    if pakid:
        pak = ThreePak.objects.get(id=pakid)
        return pak.id

    try:
        team = request.user.profile.customer
        game = get_next_or_current_game(team)
        if game:
            pak, created = ThreePak.objects.get_or_create(
                user=request.user,
                GameID=game.GameID
            )
            return pak.id
        return None
    except Exception as e:
        logger.error("Exception in get_pakid: {}".format(e))
    return None


@api_view(['GET', 'POST'])
def my_picks(request):
    player_type = ContentType.objects.get_for_model(PlayerGameProjectionMLB)
    team_type = ContentType.objects.get_for_model(TeamGameMLB)

    try:
        pakid = get_pakid(request)
        
        if not pakid:
            return JsonResponse({'picks': []}, safe=False)
        
        pak = ThreePak.objects.get(id=pakid) 
        picks = pak.get_picks()
        res = []
        for p in picks:
            obj_type = ContentType.objects.get_for_model(p.content_object)
            if obj_type == player_type:
                res.append(PlayerGameProjectionMLBSerializer(p.content_object).data)
            elif obj_type == team_type:
                res.append(TeamGameMLBSerializer(p.content_object).data)

        respak = {'picks': res, '3pak': pak.id}
        return JsonResponse(respak, safe=False)
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code, 'picks': []})


@api_view(['GET', 'POST'])
def game_details(request):
    u = request.user
    try:
        pakid = request.GET.get('3pak', None)

        try:
            contest = Contest.objects.get(threepaks=pakid)
        except BaseException:
            pak = ThreePak.objects.get(id=pakid)

            # TODO  must revisit
            now = timezone.localtime(timezone.now())

            # betaspec = TournamentSpec.objects.get(cost=3,guaranteed_payout=140)
            # bcnt = ThreePak.objects.filter(contest__spec_id=betaspec.id).count()

            specialstart, specialend = promo_range(now)
            # if (now > specialstart) and (now < specialend) and (bcnt<100):
            # ts = betaspec
            # None
            # else:
            ts = TournamentSpec.objects.first()

            # temp solution - last minute hack
            # Game Details must not require a contest...
            ret = {'contest_id': 0,
                   'gt_prizes': ts.guaranteed_payout,
                   'entry_fee': ts.cost,
                   'num_players': ts.max_players,
                   'total_players': ts.max_players,
                #    'nfl_weeks': (pak.start_week, pak.start_week + 1)
                   }
            return JsonResponse(ret)
        ret = {'contest_id': contest.id,
               'gt_prizes': contest.spec.guaranteed_payout,
               'entry_fee': contest.entry_fee,
               'num_players': contest.num_players,
               'total_players': contest.spec.max_players,
            #    'nfl_weeks': contest.nfl_weeks
               }
        return JsonResponse(ret)
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})


@api_view(['POST', ])
def make_pick(request):

    team = request.user.profile.customer
    game = get_next_or_current_game(team)
    
    # For API user definitions
    PLAYERGAME = 1
    # we need the user...
    u = request.user
    try:
        # we need the type of object
        t = int(request.POST.get('type', 0))
        
        # we need the id of object to add
        id = int(request.POST.get('id', 0))

        pak, created = ThreePak.objects.get_or_create(
            user=u,
            GameID=game.GameID
        )
        
        obj = PlayerGameProjectionMLB.objects.get(id=id)    
        pak.make_pick(obj, pak.id)
        
        return JsonResponse({'3pak': pak.id, 'success': 'added %s' % obj})
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})


@api_view(['POST', ])
def remove_pick(request):
    # For API user definitions
    PLAYERGAME = 1
    TEAMGAME = 2
    try:
        pak = ThreePak.objects.get(id=request.POST.get('3pak', 0))
        if pak == 0:
            # To be more fault resiliant, if 3pak is missing, try to pull
            # one for the user in the current session.  This rule may not
            # be valid in future releases, so review.

            # cweek = get_current_week()

            # packs = ThreePak.objects.filter(Q(start_week=cweek.Week) | Q(
            #     start_week=cweek.Week - 1), user=request.user)
            packs = ThreePak.objects.filter(user=request.user)
            if len(packs):
                pakid = packs.last().id

        id = request.POST.get('id', None)
        t = request.POST.get('api_type', None)
        if (int(t) == PLAYERGAME):
            obj = PlayerGameProjectionMLB.objects.get(id=id)
        elif (int(t) == TEAMGAME):
            obj = TeamGameMLB.objects.get(id=id)

        # cweek = get_current_week()
        id = obj.id
        obj_type = ContentType.objects.get_for_model(obj)
        obj = Pick.objects.get(
            threepak=pak,
            object_id=id,
            content_type=obj_type,
            # session_week=cweek.Week
            )

        obj.delete()

        #you_need_three_warning.apply_async((pak,), countdown=(30 * 60))
        return JsonResponse({'success': 'Removed pick'})
    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})

@api_view(['POST'])
def invite_user(request):
    try:
        email1 = request.POST.get('email1')
        email2 = request.POST.get('email2')
        email3 = request.POST.get('email3')
        if email1:
            Invite.objects.get_or_create(
                user=request.user,
                address=email1
            )
        if email2:
            Invite.objects.get_or_create(
                user=request.user,
                address=email2
            )
        if email3:
            Invite.objects.get_or_create(
                user=request.user,
                address=email3
            )
        return JsonResponse({'success': True})

    except Exception as ex:
        try:
            code = ex.err_code()
        except BaseException:
            code = -1
        return JsonResponse({'error': ex.message, 'error_code': code})


@api_view(['POST'])
def user_in_fence(request):
    """ Checks to see if user is in a GEO fence.  If not configures or 
    incomplete data, silently fails and returns in_fence is false
    """
    
    try:
        lat = request.POST.get('latitude') 
        long = request.POST.get('longitude')

        if not lat or not long:
            return JsonResponse({'in_fence': False,
                                 'msg': ""})
     
        latitude = decimal.Decimal(lat)
        longitude = decimal.Decimal(long)
        user_profile = request.user.profile.customer

        geos = GEOFence.objects.filter(profiles=user_profile)
        msg = ""
        inside_fence = False
        for geo in geos:
            state, created = FenceState.objects.get_or_create(user=request.user,
                                                              fence=geo)

            inside_fence = in_fence(geo, latitude, longitude)
            msg = ""
            if inside_fence and not state.inside:
                msg = geo.enter_msg
                state.inside = True
                state.save()
                break
            elif not inside_fence and state.inside:
                msg = geo.exit_msg
                state.inside = False
                state.save()
                break

        
        return JsonResponse({'in_fence': inside_fence,
                                 'msg': msg})


    except Exception as ex:
        pass

    return JsonResponse({'in_fence': False,
        'msg': ""})
    

def in_fence(geo, latitude, longitude):
    dataset = Point.objects.filter(fence_id__id=geo.id).order_by('order')
    lats_longs_vect = dataset.values_list('x', 'y')
    # print(lats_longs_vect)

    polygon = Polygon(lats_longs_vect)
    point = shapelyPoint(latitude, longitude)
    _in = polygon.contains(point)

    return _in


class LoginAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
