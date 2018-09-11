import requests
from django.conf import settings
from datetime import datetime
from app.models import (
    TeamMLB,
    StadiumMLB,
    GameMLB,
    PlayerMLB,
    PlayerGameMLB,
    TeamGameMLB,
    PlayerSeasonMLB,
    TeamSeasonMLB,
    NewsMLB,
    PlayerGameProjectionMLB,
    PlayerSeasonProjectionMLB,
    StandingMLB,
    DfsSlateMLB,
    DfsSlateGameMLB,
    DfsSlatePlayerMLB,
    InningMLB,
    BoxScoreMLB,
    ScheduleMLB,
)

def fill_date(date):
    if not date:
        return datetime.now().date().strftime('%Y-%b-%d')
    return date

def fill_year(year):
    
    if not year:
        return datetime.now().date().strftime('%Y')
    return year  

class Mlb(object):
    base_url = "https://api.fantasydata.net/v{version}/mlb/stats/JSON/{api}?key={key}"
    api_version = 3

    def call_api(self, api):
        uri = self.base_url.format(version=self.api_version, api=api, key=settings.FANTASY_DATA_KEY_MLB)
        print uri
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise Exception(resp.status_code)

        results = resp.json()
        # print results
        return results

    def create_teams(self):
        teams = self.call_api('teams')

        for team in teams:
            print team

            obj, created = TeamMLB.objects.update_or_create(
                TeamID=team.get('TeamID'),
                defaults=team
            )

    def create_stadiums(self):
        stadiums = self.call_api('Stadiums')

        for stadium in stadiums:
            print stadium

            obj, created = StadiumMLB.objects.update_or_create(
                StadiumID=stadium.get('StadiumID'),
                defaults=stadium
            )

    # fetches Active Players
    def create_players(self):
        players = self.call_api('Players')

        for player in players:
            print player

            obj, created = PlayerMLB.objects.update_or_create(
                PlayerID=player.get('PlayerID'),
                defaults=player
            )

    # date : string  (The date of the game(s). Examples: 2017-JUL-31, 2017-SEP-01.)
    def save_games(self, date):
        games = self.call_api('GamesByDate/{}'.format(fill_date(date)))

        for game in games:
            # print game

            obj, created = GameMLB.objects.update_or_create(
                GameID=game.get('GameID'),
                defaults=game
            )

    # date : string  (The date of the game(s). Examples: 2017-JUL-31, 2017-SEP-01.)
    def save_player_games(self, date):
        player_games = self.call_api('PlayerGameStatsByDate/{}'.format(fill_date(date)))

        for player_game in player_games:
            print player_game

            obj, created = PlayerGameMLB.objects.update_or_create(
                PlayerID=player_game.get('PlayerID'),
                GameID=player_game.get('GameID'),
                defaults=player_game
            )

    # date : string  (The date of the game(s). Examples: 2017-JUL-31, 2017-SEP-01.)
    def save_team_games(self, date):
        team_games = self.call_api('TeamGameStatsByDate/{}'.format(fill_date(date)))

        for team_game in team_games:
            print team_game

            obj, created = TeamGameMLB.objects.update_or_create(
                StatID=team_game.get('StatID'),
                defaults=team_game
            )

    # season : string  (Year of the season. Examples: 2017, 2018.)
    def save_player_seasons(self, season):
        player_seasons = self.call_api('PlayerSeasonStats/{}'.format(fill_year(season)))

        for player_season in player_seasons:
            print player_season

            obj, created = PlayerSeasonMLB.objects.update_or_create(
                StatID=player_season.get('StatID'),
                defaults=player_season
            )

    # season : string  (Year of the season. Examples: 2017, 2018.)
    def save_team_seasons(self, season):
        team_seasons = self.call_api('TeamSeasonStats/{}'.format(fill_year(season)))

        for team_season in team_seasons:
            print team_season

            obj, created = TeamSeasonMLB.objects.update_or_create(
                StatID=team_season.get('StatID'),
                defaults=team_season
            )

    def create_news(self):
        mlb_news = self.call_api('News')

        for news in mlb_news:
            print news

            obj, created = NewsMLB.objects.update_or_create(
                NewsID=news.get('NewsID'),
                defaults=news
            )

    # season : string  (Year of the season. Examples: 2017, 2018.)
    def save_standings(self, season):
        standings = self.call_api('Standings/{}'.format(fill_year(season)))

        for standing in standings:
            print standing

            obj, created = StandingMLB.objects.update_or_create(
                Season=standing.get('Season'),
                TeamID=standing.get('TeamID'),
                defaults=standing
            )

    # date : string  (The date of the slates. Examples: 2017-JUL-31, 2017-SEP-01.)
    def save_dfs_slates(self, date):
        
        
        dfs_slates = self.call_api('DfsSlatesByDate/{}'.format(fill_date(date)))

        for slate in dfs_slates:
            print slate

            obj, created = DfsSlateMLB.objects.update_or_create(
                SlateID=slate.get('SlateID'),
            )
            obj.Operator=slate.get('Operator'),
            obj.OperatorSlateID=slate.get('OperatorSlateID'),
            obj.OperatorName=slate.get('OperatorName'),
            obj.OperatorDay=slate.get('OperatorDay'),
            obj.OperatorStartTime=slate.get('OperatorStartTime'),
            obj.NumberOfGames=slate.get('NumberOfGames'),
            obj.IsMultiDaySlate=slate.get('IsMultiDaySlate'),
            obj.RemovedByOperator=slate.get('RemovedByOperator'),
            obj.OperatorGameType=slate.get('OperatorGameType'),
            obj.save()
             
            games = slate.get('DfsSlateGames')
            for game in games:
               game_obj, game_created = DfsSlateGameMLB.objects.update_or_create(
                   SlateGameID=game.get('SlateGameID'),
                   defaults=game
               )
               obj.DfsSlateGames.add(game_obj)

            players = slate.get('DfsSlatePlayers')
            for player in players:
                player_obj, player_created = DfsSlatePlayerMLB.objects.update_or_create(
                    SlatePlayerID=player.get('SlatePlayerID'),
                    defaults=player
                )
                obj.DfsSlatePlayers.add(player_obj)


    # date : string  (The date of the game(s). Examples: 2017-JUL-31, 2017-SEP-01.)
    def save_box_scores(self, date):
        box_scores = self.call_api('BoxScores/{}'.format(fill_date(date)))

        for box_score in box_scores:
            game=box_score.get('Game')

            obj, created = GameMLB.objects.update_or_create(
                GameID=game.get('GameID'),
                defaults=game
            )
            # if created:
            #     obj_box = BoxScoreMLB.objects.create(Game=obj)

            obj_box, obj_box_created = BoxScoreMLB.objects.update_or_create(
                Game=obj,
            )

            innings = box_score.get('Innings')
            for inning in innings:
                inning_obj, inning_created = InningMLB.objects.update_or_create(
                    GameID=inning.get('GameID'),
                    defaults=inning
                )
                print inning_created
                obj_box.Innings.add(inning_obj)

            team_games = box_score.get('TeamGames')
            for team_game in team_games:
                team_game_obj, team_game_created = TeamGameMLB.objects.update_or_create(
                    StatID=team_game.get('StatID'),
                    defaults=team_game
                )
                obj_box.TeamGames.add(team_game_obj)

            player_games = box_score.get('PlayerGames')
            for player_game in player_games:
                player_game_obj, player_game_created = PlayerGameMLB.objects.update_or_create(
                    PlayerID=player_game.get('PlayerID'),
                    GameID=player_game.get('GameID'),
                    defaults=player_game
                )
                obj_box.PlayerGames.add(player_game_obj)


class MlbProjection(object):
    base_url = "https://api.fantasydata.net/v{version}/mlb/projections/JSON/{api}?key={key}"
    api_version = 3

    def call_api(self, api):
        uri = self.base_url.format(version=self.api_version, api=api, key=settings.FANTASY_DATA_PROJECTIONS_KEY_MLB)
        print uri
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise Exception(resp.status_code)

        results = resp.json()
        print results
        return results

    # date : string  (The date of the game(s). Examples: 2017-JUL-31, 2017-SEP-01.)
    def save_player_game_projection(self, date=None):       
        
        player_game_projections = self.call_api('PlayerGameProjectionStatsByDate/{}'.format(fill_date(date)))

        for player_game_projection in player_game_projections:
            print player_game_projection

            obj, created = PlayerGameProjectionMLB.objects.update_or_create(
                StatID=player_game_projection.get('StatID'),
                defaults=player_game_projection
            )

    # season : string  (Year of the season. Examples: 2017, 2018.)
    def save_player_season_projection(self, season):
        player_season_projections = self.call_api('PlayerSeasonProjectionStats/{}'.format(fill_year(season)))

        for player_season_projection in player_season_projections:
            print player_season_projection

            obj, created = PlayerSeasonProjectionMLB.objects.update_or_create(
                StatID=player_season_projection.get('StatID'),
                defaults=player_season_projection
            )



class MlbScore(object):
    base_url = "https://api.fantasydata.net/v{version}/mlb/scores/JSON/{api}?key={key}"
    api_version = 3

    def call_api(self, api):
        uri = self.base_url.format(version=self.api_version, api=api, key=settings.FANTASY_DATA_KEY_MLB)
        print uri
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise Exception(resp.status_code)

        results = resp.json()
        print results
        return results

    # season : string  (Year of the season (with optional season type). Examples: 2018, 2018PRE, 2018POST, 2018STAR,
    #  2019, etc.)
    def save_schedules(self, season):
        schedules = self.call_api('Games/{}'.format(fill_year(season)))

        for schedule in schedules:
            print schedule

            obj, created = ScheduleMLB.objects.update_or_create(
                GameID=schedule.get('GameID'),
                defaults=schedule
            )