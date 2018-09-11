from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from app.views import (
   UserViewSet,
   CustomerProfileViewSet,
   TournamentSpecViewSet,
   TournamentPlacementViewSet,
   pick_window_open,
   window_info,
   make_pick,
   dashboard,
   is_stripe_registered,
   payment_received,
   register_stripe_token,
   start_contest,
   set_card_name,
   my_picks,
   remove_pick,
   game_details,
   invite_user,
   LoginAuthToken,
   user_in_fence,
   leaderboard,
    TeamMLBViewSet,
    StadiumMLBViewSet,
    GameMLBViewSet,
    PlayerMLBViewSet,
    PlayerGameMLBViewSet,
    TeamGameMLBViewSet,
    PlayerSeasonMLBViewSet,
    TeamSeasonMLBViewSet,
    NewsMLBViewSet,
    PlayerGameProjectionMLBViewSet,
    PlayerSeasonProjectionMLBViewSet,
    StandingMLBViewSet,
    DfsSlatePlayerMLBViewSet,
    DfsSlateGameMLBViewSet,
    DfsSlateMLBViewSet,
    InningMLBViewSet,
    BoxScoreMLBViewSet,
    ScheduleMLBViewSet,
    )
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'customerprofiles', CustomerProfileViewSet)

router.register(r'mlb_teams', TeamMLBViewSet)
router.register(r'mlb_stadiums', StadiumMLBViewSet)
router.register(r'mlb_games', GameMLBViewSet)
router.register(r'mlb_players', PlayerMLBViewSet)
router.register(r'mlb_player_games', PlayerGameMLBViewSet, base_name="playergamemlb")
router.register(r'mlb_team_games', TeamGameMLBViewSet)
router.register(r'mlb_player_seasons', PlayerSeasonMLBViewSet)
router.register(r'mlb_team_seasons', TeamSeasonMLBViewSet)
router.register(r'mlb_news', NewsMLBViewSet)
router.register(r'mlb_player_game_projections', PlayerGameProjectionMLBViewSet, base_name="playergameprojectionmlb")
router.register(r'mlb_player_season_projections', PlayerSeasonProjectionMLBViewSet)
router.register(r'mlb_standings', StandingMLBViewSet)
router.register(r'mlb_dfs_slate_players', DfsSlatePlayerMLBViewSet)
router.register(r'mlb_dfs_slate_games', DfsSlateGameMLBViewSet)
router.register(r'mlb_dfs_slates', DfsSlateMLBViewSet)
router.register(r'mlb_innings', InningMLBViewSet)
router.register(r'mlb_box_scores', BoxScoreMLBViewSet)
router.register(r'mlb_schedules', ScheduleMLBViewSet, base_name="schedulemlb")
router.register(r'tournamentspecs', TournamentSpecViewSet)
router.register(r'tournamentplacement', TournamentPlacementViewSet)

urlpatterns = [
    url(r'^is_pick_window_open/$', pick_window_open),
    url(r'^window_info/$', window_info),
    url(r'^make_pick/$', make_pick),
    url(r'^dashboard/$', dashboard),
    url(r'^is_stripe_registered/$', is_stripe_registered),
    url(r'^payment_received/$', payment_received),
    url(r'^register_stripe_token/$', register_stripe_token),
    url(r'^start_contest/$', start_contest),
    url(r'^set_card_name/$', set_card_name),
    url(r'^my_picks/$', my_picks),
    url(r'^remove_pick/$', remove_pick),
    url(r'^game_details/$', game_details),
    url(r'^invite_user/$', invite_user),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', LoginAuthToken.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # new for 2017 below
    url(r'^leaderboard/(?P<customer>[\w-]+)/$', leaderboard),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^user_in_fence/$', user_in_fence),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


