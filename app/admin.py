from django.contrib import admin
from app.models import *
from django import forms
from gfklookupwidget.widgets import GfkLookupWidget 


class MyUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email',)
    list_display = ('username', 'email', 'date_joined', 'first_name',
                    'last_name')


class ThreePakAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created', 'updated')
    search_fields = ('user__username',)


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'league',)
    fieldsets = (
        (None, {
            'fields': ('league', 'name', 'happy_name',)
        }),
        ('Leaderboard adjustments', {
            'fields': ('color_primary',
                       'color_secondary',
                       'button_font_color',
                       'color_3',
                       'color_4',
                       'color_5',
                       'color_6',
                       'color_7',
                       'color_lhb',
                       'color_rhb',
                       'color_lhb_2',
                       'color_rhb_2',
                       'logo_large',
                       'logo_small',
                       'header_background',
                       'header_title',
                       'header_title_2',
                       'header_title_padding',
                       'header_title_2_padding',
                       'subtitle',
                       'subtitle_2',
                       'footer_text',
                       'page_ad',
                       'page_ad_2',
                       'page_ad_3',
                       'page_ad_4',
                       'page_ad_style',
                       'leader_header_advertisement',
                       'leader_header_advertisement_2',
                       )
        }),
        ('Web App', {
            'fields': ('prize_1',
                       'prize_2',
                       'prize_3',
                       'advertisement',
                       'advertisement_2',
                       'advertisement_uri',
                       'advertisement_uri_2',
                       'prize_top_label_1',
                       'prize_top_label_2',
                       'prize_top_label_3',
                       'prize_label_1',
                       'prize_label_2',
                       'prize_label_3',)
        }),
        (None, {
            'fields': ('promo_blurb',
                       'show_quadbox',
                       'dark_fonts',
                       'quadbox_img',
                       'min_age_to_play',
                       'location_required',)
        }),
    )



class PickForm(forms.ModelForm):
    class Meta(object):
        model = Pick
        fields = ('threepak', 'content_type', 'object_id', 'session_week',)
        widgets = {
            'object_id': GfkLookupWidget(
                content_type_field_name='content_type',
                parent_field=Pick._meta.get_field('content_type'),
            )
        }


class PickAdmin(admin.ModelAdmin):
    form = PickForm
    search_fields = ('threepak__user__username',)
    list_display = ('threepak', 'created', 'updated',)

class PointsInline(admin.TabularInline):
    model = Point 

class GEOFenceAdmin(admin.ModelAdmin):
    inlines = [
        PointsInline,
    ]
    list_display = ('name', 'enter_msg', 'exit_msg')


class TeamMLBAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'TeamID', 'Active', 'Division')
    search_fields = ('TeamID', 'Name')


class StadiumMLBAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'StadiumID', 'Active', 'City', 'State', 'Capacity', 'Type')
    search_fields = ('StadiumID', 'Name', 'City',)


class GameMLBAdmin(admin.ModelAdmin):
    list_display = ('GameID', 'Status', 'DateTime', 'AwayTeam', 'HomeTeam',
                    'Inning', 'InningHalf', 'AwayTeamRuns', 'HomeTeamRuns', 'AwayTeamHits', 'HomeTeamHits',
                    'AwayTeamErrors', 'HomeTeamErrors', 'Updated')
    search_fields = ('GameID', 'Status', 'DateTime', 'HomeTeam', 'AwayTeam',)


class PlayerMLBAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'PlayerID', 'Status', 'TeamID', 'Team', 'Jersey', 'Position', 'BatHand', 'ThrowHand',
                    'Experience')
    search_fields = ('PlayerID', 'Status', 'TeamID', 'Team', 'Jersey',)


class PlayerGameMLBAdmin(admin.ModelAdmin):
    list_display = ('TeamID', 'PlayerID', 'Season', 'Name', 'Team', 'Position', 'BattingOrder',
                    'FanDuelSalary', 'DraftKingsSalary', 'FantasyDataSalary', 'InjuryStatus', 'InjuryBodyPart',
                    'FantasyDraftSalary', 'Opponent', 'HomeOrAway',
                    'IsGameOver', 'Updated', 'Games', 'FantasyPoints', 'Runs', 'Hits', 'Singles', 'Doubles', 'Triples',
                    'HomeRuns', 'Wins', 'Losses', 'Saves', 'FantasyPointsFanDuel', 'FantasyPointsDraftKings',
                    'FantasyPointsYahoo')
    search_fields = ('StatID', 'PlayerID', 'Season', 'TeamID', 'Team', 'Name', )


class TeamGameMLBAdmin(admin.ModelAdmin):
    list_display = ('TeamID', 'Season', 'Name', 'Team', 'Opponent', 'DateTime', 'HomeOrAway',
                    'IsGameOver', 'Updated', 'Games', 'FantasyPoints', 'Runs', 'Hits', 'Singles', 'Doubles', 'Triples',
                    'HomeRuns', 'Errors', 'Wins', 'Losses', 'Saves', 'FantasyPointsFanDuel', 'FantasyPointsDraftKings',
                    'FantasyPointsYahoo', 'FantasyPointsFantasyDraft')
    search_fields = ('StatID', 'Season', 'TeamID', 'Team', 'Name', 'DateTime',)


class PlayerSeasonMLBAdmin(admin.ModelAdmin):
    list_display = ('TeamID', 'PlayerID', 'Season', 'Name', 'Team', 'Position',
                    'Updated', 'Games', 'FantasyPoints', 'Runs', 'Hits', 'Singles', 'Doubles', 'Triples',
                    'HomeRuns', 'Errors', 'Wins', 'Losses', 'Saves', 'FantasyPointsFanDuel', 'FantasyPointsDraftKings',
                    'FantasyPointsYahoo', 'FantasyPointsFantasyDraft')
    search_fields = ('StatID', 'PlayerID', 'Season', 'TeamID', 'Team', 'Name', )

class TeamSeasonMLBAdmin(admin.ModelAdmin):
    list_display = ('TeamID', 'Season', 'Name', 'Team', 'Updated', 'Games', 'FantasyPoints', 'Runs',
                    'Hits', 'Singles', 'Doubles', 'Triples', 'HomeRuns', 'Errors', 'Wins', 'Losses', 'Saves',
                    'FantasyPointsFanDuel', 'FantasyPointsDraftKings', 'FantasyPointsYahoo',
                    'FantasyPointsFantasyDraft')
    search_fields = ('StatID', 'Season', 'TeamID', 'Team', 'Name',)


class NewsMLBAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'NewsID', 'Source', 'Updated', 'Content', 'Url', 'Author', 'Team', 'Team2')
    search_fields = ('NewsID', 'Source', 'Title', 'Team', 'Team2')


class PlayerGameProjectionMLBAdmin(admin.ModelAdmin):
    list_display = ('DateTime', 'Team', 'Opponent', 'TeamID', 'PlayerID', 'GameID', 'Season', 'Name', 'Position',
                    'InjuryStatus', 'InjuryBodyPart', 'HomeOrAway',
                    'IsGameOver', 'Updated')
    search_fields = ('StatID', 'PlayerID', 'Season', 'GameID', 'TeamID', 'Team', 'Name', )
    list_filter = ('Position',)


class PlayerSeasonProjectionMLBAdmin(admin.ModelAdmin):
    list_display = ('TeamID', 'PlayerID', 'Season', 'Name', 'Team', 'Position',
                    'Updated', 'Games')
    search_fields = ('StatID', 'PlayerID', 'Season', 'TeamID', 'Team', 'Name', )


class StandingMLBAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'Key', 'City', 'Name', 'Division', 'Wins', 'Losses', 'Percentage',
                    'LastTenGamesWins', 'LastTenGamesLosses', 'Streak', 'HomeWins', 'HomeLosses', 'AwayWins',
                    'AwayLosses')
    search_fields = ('TeamID', 'Season', 'Name',)


class DfsSlatePlayerMLBAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'SlateID', 'SlateGameID', 'PlayerID', 'PlayerGameProjectionStatID')
    search_fields = ('SlatePlayerID', 'SlateID',)


class DfsSlateGameMLBAdmin(admin.ModelAdmin):
    list_display = ('SlateID', 'GameID', 'OperatorGameID')
    search_fields = ('SlateGameID', 'SlateID',)


class DfsSlateMLBAdmin(admin.ModelAdmin):
    list_display = ('OperatorSlateID', 'OperatorName', 'OperatorDay', 'NumberOfGames')
    search_fields = ('SlateID', 'Operator',)


class ScheduleMLBAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'Season', 'Status', 'DateTime', 'AwayTeam', 'HomeTeam')
    search_fields = ('HomeTeam', 'AwayTeam',)

class SeriesMLBAdmin(admin.ModelAdmin):
    list_display = ('series_start', 'series_end', 'AwayTeam', 'HomeTeam')
    search_fields = ('HomeTeam', 'AwayTeam',)

def schedule(obj):
    return str(ScheduleMLB.objects.get(GameID=obj.GameID)) 

class InningMLBAdmin(admin.ModelAdmin):
      
    list_display = (schedule, 'GameID', 'InningNumber', 'AwayTeamRuns', 'HomeTeamRuns', )
    search_fields = ('GameID', )

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
    
admin.site.register(Pick, PickAdmin)
admin.site.register(TournamentSpec)
admin.site.register(TournamentPlacement)
admin.site.register(Contest)
admin.site.register(News)
admin.site.register(League)
admin.site.register(Badge)
admin.site.register(Invite)
admin.site.register(UserCompany)
admin.site.register(Point)
admin.site.register(FenceState)
admin.site.register(GEOFence, GEOFenceAdmin)
admin.site.register(TeamMLB, TeamMLBAdmin)
admin.site.register(InningMLB, InningMLBAdmin)
admin.site.register(BoxScoreMLB)
admin.site.register(StadiumMLB, StadiumMLBAdmin)
admin.site.register(GameMLB, GameMLBAdmin)
admin.site.register(PlayerMLB, PlayerMLBAdmin)
admin.site.register(PlayerGameMLB, PlayerGameMLBAdmin)
admin.site.register(TeamGameMLB, TeamGameMLBAdmin)
admin.site.register(PlayerSeasonMLB, PlayerSeasonMLBAdmin)
admin.site.register(TeamSeasonMLB, TeamSeasonMLBAdmin)
admin.site.register(NewsMLB, NewsMLBAdmin)
admin.site.register(PlayerGameProjectionMLB, PlayerGameProjectionMLBAdmin)
admin.site.register(PlayerSeasonProjectionMLB, PlayerSeasonProjectionMLBAdmin)
admin.site.register(StandingMLB, StandingMLBAdmin)
admin.site.register(DfsSlatePlayerMLB, DfsSlatePlayerMLBAdmin)
admin.site.register(DfsSlateGameMLB, DfsSlateGameMLBAdmin)
admin.site.register(DfsSlateMLB, DfsSlateMLBAdmin)
admin.site.register(ScheduleMLB, ScheduleMLBAdmin)
admin.site.register(SeriesMLB, SeriesMLBAdmin)
admin.site.register(ThreePak, ThreePakAdmin)

