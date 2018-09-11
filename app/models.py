import logging
import operator
from datetime import datetime, timedelta
from django.utils import timezone
import django
import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django_mysql.models import JSONField
from mock.mock import self
from django.utils.timesince import timesince

logger = logging.getLogger(__name__)

OPEN_PICK_INNING_CUTOFF = 4


def locked(GameID):
    inning = InningMLB.objects.filter(GameID=GameID).first()

    if inning and inning.InningNumber >= OPEN_PICK_INNING_CUTOFF:
        return True
    else:
        return False


class DayOfWeek():
    """ 
    How about some constants for datetime day of week?
    """
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class League(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class TeamMLB(models.Model):
    TeamID = models.IntegerField()
    Key = models.CharField(max_length=150, default="")
    Active = models.BooleanField(default=0)
    City = models.CharField(max_length=150, null=True, blank=True)
    Name = models.CharField(max_length=150, null=True, blank=True)
    StadiumID = models.IntegerField(null=True, blank=True)
    League = models.CharField(max_length=10, null=True, blank=True)
    Division = models.CharField(max_length=10, null=True, blank=True)
    PrimaryColor = models.CharField(max_length=6, null=True, blank=True)
    SecondaryColor = models.CharField(max_length=6, null=True, blank=True)
    TertiaryColor = models.CharField(max_length=6, null=True, blank=True)
    QuaternaryColor = models.CharField(max_length=6, null=True, blank=True)
    WikipediaLogoUrl = models.CharField(max_length=250, null=True, blank=True)
    WikipediaWordMarkUrl = models.CharField(max_length=250, null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.Name


class StadiumMLB(models.Model):
    StadiumID = models.IntegerField()
    Active = models.BooleanField(default=0)
    Name = models.CharField(max_length=100, default='')
    City = models.CharField(max_length=150, null=True, blank=True)
    State = models.CharField(max_length=50, null=True, blank=True)
    Country = models.CharField(max_length=10, null=True, blank=True)
    Capacity = models.IntegerField(null=True, blank=True)
    Surface = models.CharField(max_length=50, null=True, blank=True)
    LeftField = models.IntegerField(null=True, blank=True)
    MidLeftField = models.IntegerField(null=True, blank=True)
    LeftCenterField = models.IntegerField(null=True, blank=True)
    MidLeftCenterField = models.IntegerField(null=True, blank=True)
    CenterField = models.IntegerField(null=True, blank=True)
    MidRightCenterField = models.IntegerField(null=True, blank=True)
    RightCenterField = models.IntegerField(null=True, blank=True)
    MidRightField = models.IntegerField(null=True, blank=True)
    RightField = models.IntegerField(null=True, blank=True)
    GeoLat = models.FloatField(null=True, blank=True)
    GeoLong = models.FloatField(null=True, blank=True)
    Altitude = models.IntegerField(null=True, blank=True)
    HomePlateDirection = models.IntegerField(null=True, blank=True)
    Type = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.Name


class GameMLB(models.Model):

    def __unicode__(self):
        return "{} {}".format(self.GameID, self.Day)

    GameID = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField()
    SeasonType = models.IntegerField()
    Status = models.CharField(max_length=20, null=True, blank=True)
    Day = models.DateTimeField(null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    AwayTeam = models.CharField(max_length=10, default='')
    HomeTeam = models.CharField(max_length=10, default='')
    AwayTeamID = models.IntegerField(null=True, blank=True)
    HomeTeamID = models.IntegerField(null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    RescheduledGameID = models.IntegerField(null=True, blank=True)
    StadiumID = models.IntegerField(null=True, blank=True)
    Channel = models.CharField(max_length=100, null=True, blank=True)
    Inning = models.IntegerField(null=True, blank=True)
    InningHalf = models.CharField(max_length=1, null=True, blank=True)
    AwayTeamRuns = models.IntegerField(null=True, blank=True)
    HomeTeamRuns = models.IntegerField(null=True, blank=True)
    AwayTeamHits = models.IntegerField(null=True, blank=True)
    HomeTeamHits = models.IntegerField(null=True, blank=True)
    AwayTeamErrors = models.IntegerField(null=True, blank=True)
    HomeTeamErrors = models.IntegerField(null=True, blank=True)
    WinningPitcherID = models.IntegerField(null=True, blank=True)
    LosingPitcherID = models.IntegerField(null=True, blank=True)
    SavingPitcherID = models.IntegerField(null=True, blank=True)
    Attendance = models.IntegerField(null=True, blank=True)
    AwayTeamProbablePitcherID = models.IntegerField(null=True, blank=True)
    HomeTeamProbablePitcherID = models.IntegerField(null=True, blank=True)
    Outs = models.IntegerField(null=True, blank=True)
    Balls = models.IntegerField(null=True, blank=True)
    Strikes = models.IntegerField(null=True, blank=True)
    CurrentPitcherID = models.IntegerField(null=True, blank=True)
    CurrentHitterID = models.IntegerField(null=True, blank=True)
    AwayTeamStartingPitcherID = models.IntegerField(null=True, blank=True)
    HomeTeamStartingPitcherID = models.IntegerField(null=True, blank=True)
    CurrentPitchingTeamID = models.IntegerField(null=True, blank=True)
    CurrentHittingTeamID = models.IntegerField(null=True, blank=True)
    PointSpread = models.FloatField(null=True, blank=True)
    OverUnder = models.FloatField(null=True, blank=True)
    AwayTeamMoneyLine = models.IntegerField(null=True, blank=True)
    HomeTeamMoneyLine = models.IntegerField(null=True, blank=True)
    ForecastTempLow = models.IntegerField(null=True, blank=True)
    ForecastTempHigh = models.IntegerField(null=True, blank=True)
    ForecastDescription = models.CharField(max_length=50, null=True, blank=True)
    ForecastWindChill = models.IntegerField(null=True, blank=True)
    ForecastWindSpeed = models.IntegerField(null=True, blank=True)
    ForecastWindDirection = models.IntegerField(null=True, blank=True)
    RescheduledFromGameID = models.IntegerField(null=True, blank=True)
    RunnerOnFirst = models.NullBooleanField()
    RunnerOnSecond = models.NullBooleanField()
    RunnerOnThird = models.NullBooleanField()
    AwayTeamStartingPitcher = models.CharField(max_length=50, null=True, blank=True)
    HomeTeamStartingPitcher = models.CharField(max_length=50, null=True, blank=True)
    CurrentPitcher = models.CharField(max_length=50, null=True, blank=True)
    CurrentHitter = models.CharField(max_length=50, null=True, blank=True)
    WinningPitcher = models.CharField(max_length=50, null=True, blank=True)
    LosingPitcher = models.CharField(max_length=50, null=True, blank=True)
    SavingPitcher = models.CharField(max_length=50, null=True, blank=True)
    DueUpHitterID1 = models.IntegerField(null=True, blank=True)
    DueUpHitterID2 = models.IntegerField(null=True, blank=True)
    DueUpHitterID3 = models.IntegerField(null=True, blank=True)
    GlobalGameID = models.IntegerField(null=True, blank=True)
    GlobalAwayTeamID = models.IntegerField(null=True, blank=True)
    GlobalHomeTeamID = models.IntegerField(null=True, blank=True)
    PointSpreadAwayTeamMoneyLine = models.IntegerField(null=True, blank=True)
    PointSpreadHomeTeamMoneyLine = models.IntegerField(null=True, blank=True)
    LastPlay = models.CharField(max_length=250, null=True, blank=True)
    IsClosed = models.BooleanField(default=0)
    Updated = models.DateTimeField(null=True, blank=True)


class PlayerMLB(models.Model):
    PlayerID = models.IntegerField(null=True, blank=True)

    # Deprecated. Use SportRadarPlayerID instead.
    SportsDataID = models.CharField(max_length=50, null=True, blank=True)

    Status = models.CharField(max_length=50, null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    Jersey = models.IntegerField(null=True, blank=True)
    PositionCategory = models.CharField(max_length=10, null=True, blank=True)
    Position = models.CharField(max_length=10, null=True, blank=True)
    MLBAMID = models.IntegerField(null=True, blank=True)
    FirstName = models.CharField(max_length=50, null=True, blank=True)
    LastName = models.CharField(max_length=50, null=True, blank=True)
    BatHand = models.CharField(max_length=1, null=True, blank=True)
    ThrowHand = models.CharField(max_length=1, null=True, blank=True)
    Height = models.IntegerField(null=True, blank=True)
    Weight = models.IntegerField(null=True, blank=True)
    BirthDate = models.DateTimeField(null=True, blank=True)
    BirthCity = models.CharField(max_length=50, null=True, blank=True)
    BirthState = models.CharField(max_length=50, null=True, blank=True)
    BirthCountry = models.CharField(max_length=50, null=True, blank=True)
    HighSchool = models.CharField(max_length=50, null=True, blank=True)
    College = models.CharField(max_length=50, null=True, blank=True)
    ProDebut = models.DateTimeField(null=True, blank=True)
    Salary = models.IntegerField(null=True, blank=True)
    PhotoUrl = models.CharField(max_length=250, null=True, blank=True)
    SportRadarPlayerID = models.CharField(max_length=50, null=True, blank=True)
    RotoworldPlayerID = models.IntegerField(null=True, blank=True)
    RotoWirePlayerID = models.IntegerField(null=True, blank=True)
    FantasyAlarmPlayerID = models.IntegerField(null=True, blank=True)
    StatsPlayerID = models.IntegerField(null=True, blank=True)
    SportsDirectPlayerID = models.IntegerField(null=True, blank=True)
    XmlTeamPlayerID = models.IntegerField(null=True, blank=True)
    InjuryStatus = models.CharField(max_length=50, null=True, blank=True)
    InjuryBodyPart = models.CharField(max_length=50, null=True, blank=True)
    InjuryStartDate = models.DateTimeField(null=True, blank=True)
    InjuryNotes = models.CharField(max_length=250, null=True, blank=True)
    FanDuelPlayerID = models.IntegerField(null=True, blank=True)
    DraftKingsPlayerID = models.IntegerField(null=True, blank=True)
    YahooPlayerID = models.IntegerField(null=True, blank=True)
    UpcomingGameID = models.IntegerField(null=True, blank=True)
    FanDuelName = models.CharField(max_length=50, null=True, blank=True)
    DraftKingsName = models.CharField(max_length=50, null=True, blank=True)
    YahooName = models.CharField(max_length=50, null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    FantasyDraftName = models.CharField(max_length=50, null=True, blank=True)
    FantasyDraftPlayerID = models.IntegerField(null=True, blank=True)
    Experience = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return u"{} {}".format(self.FirstName, self.LastName)


class PlayerGameMLB(models.Model):
    @property
    def locked(self):
        return locked(self.GameID)

    StatID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    PlayerID = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    Position = models.CharField(max_length=10, null=True, blank=True)
    PositionCategory = models.CharField(max_length=10, null=True, blank=True)
    Started = models.IntegerField(null=True, blank=True)
    BattingOrder = models.IntegerField(null=True, blank=True)
    FanDuelSalary = models.IntegerField(null=True, blank=True)
    DraftKingsSalary = models.IntegerField(null=True, blank=True)
    FantasyDataSalary = models.IntegerField(null=True, blank=True)
    YahooSalary = models.IntegerField(null=True, blank=True)
    InjuryStatus = models.CharField(max_length=50, null=True, blank=True)
    InjuryBodyPart = models.CharField(max_length=50, null=True, blank=True)
    InjuryStartDate = models.DateTimeField(null=True, blank=True)
    InjuryNotes = models.CharField(max_length=250, null=True, blank=True)
    FanDuelPosition = models.CharField(max_length=10, null=True, blank=True)
    DraftKingsPosition = models.CharField(max_length=10, null=True, blank=True)
    YahooPosition = models.CharField(max_length=10, null=True, blank=True)
    OpponentRank = models.IntegerField(null=True, blank=True)
    OpponentPositionRank = models.IntegerField(null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    FantasyDraftSalary = models.IntegerField(null=True, blank=True)
    FantasyDraftPosition = models.CharField(max_length=10, null=True, blank=True)
    GameID = models.IntegerField(null=True, blank=True)
    OpponentID = models.IntegerField(null=True, blank=True)
    Opponent = models.CharField(max_length=10, null=True, blank=True)
    Day = models.DateTimeField(null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    HomeOrAway = models.CharField(max_length=4, null=True, blank=True)
    IsGameOver = models.BooleanField(default=0)
    GlobalGameID = models.IntegerField(null=True, blank=True)
    GlobalOpponentID = models.IntegerField(null=True, blank=True)
    Updated = models.DateTimeField(null=True, blank=True)
    Games = models.IntegerField(null=True, blank=True)
    FantasyPoints = models.FloatField(null=True, blank=True)
    AtBats = models.FloatField(null=True, blank=True)
    Runs = models.FloatField(null=True, blank=True)
    Hits = models.FloatField(null=True, blank=True)
    Singles = models.FloatField(null=True, blank=True)
    Doubles = models.FloatField(null=True, blank=True)
    Triples = models.FloatField(null=True, blank=True)
    HomeRuns = models.FloatField(null=True, blank=True)
    RunsBattedIn = models.FloatField(null=True, blank=True)
    BattingAverage = models.FloatField(null=True, blank=True)
    Outs = models.FloatField(null=True, blank=True)
    Strikeouts = models.FloatField(null=True, blank=True)
    Walks = models.FloatField(null=True, blank=True)
    HitByPitch = models.FloatField(null=True, blank=True)
    Sacrifices = models.FloatField(null=True, blank=True)
    SacrificeFlies = models.FloatField(null=True, blank=True)
    GroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    StolenBases = models.FloatField(null=True, blank=True)
    CaughtStealing = models.FloatField(null=True, blank=True)
    PitchesSeen = models.FloatField(null=True, blank=True)
    OnBasePercentage = models.FloatField(null=True, blank=True)
    SluggingPercentage = models.FloatField(null=True, blank=True)
    OnBasePlusSlugging = models.FloatField(null=True, blank=True)
    Errors = models.FloatField(null=True, blank=True)
    Wins = models.FloatField(null=True, blank=True)
    Losses = models.FloatField(null=True, blank=True)
    Saves = models.FloatField(null=True, blank=True)
    InningsPitchedDecimal = models.FloatField(null=True, blank=True)
    TotalOutsPitched = models.FloatField(null=True, blank=True)
    InningsPitchedFull = models.FloatField(null=True, blank=True)
    InningsPitchedOuts = models.FloatField(null=True, blank=True)
    EarnedRunAverage = models.FloatField(null=True, blank=True)
    PitchingHits = models.FloatField(null=True, blank=True)
    PitchingRuns = models.FloatField(null=True, blank=True)
    PitchingEarnedRuns = models.FloatField(null=True, blank=True)
    PitchingWalks = models.FloatField(null=True, blank=True)
    PitchingStrikeouts = models.FloatField(null=True, blank=True)
    PitchingHomeRuns = models.FloatField(null=True, blank=True)
    PitchesThrown = models.FloatField(null=True, blank=True)
    PitchesThrownStrikes = models.FloatField(null=True, blank=True)
    WalksHitsPerInningsPitched = models.FloatField(null=True, blank=True)
    PitchingBattingAverageAgainst = models.FloatField(null=True, blank=True)
    GrandSlams = models.FloatField(null=True, blank=True)
    FantasyPointsFanDuel = models.FloatField(null=True, blank=True)
    FantasyPointsDraftKings = models.FloatField(null=True, blank=True)
    FantasyPointsYahoo = models.FloatField(null=True, blank=True)
    PlateAppearances = models.FloatField(null=True, blank=True)
    TotalBases = models.FloatField(null=True, blank=True)
    FlyOuts = models.FloatField(null=True, blank=True)
    GroundOuts = models.FloatField(null=True, blank=True)
    LineOuts = models.FloatField(null=True, blank=True)
    PopOuts = models.FloatField(null=True, blank=True)
    IntentionalWalks = models.FloatField(null=True, blank=True)
    ReachedOnError = models.FloatField(null=True, blank=True)
    BallsInPlay = models.FloatField(null=True, blank=True)
    BattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    WeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSingles = models.FloatField(null=True, blank=True)
    PitchingDoubles = models.FloatField(null=True, blank=True)
    PitchingTriples = models.FloatField(null=True, blank=True)
    PitchingGrandSlams = models.FloatField(null=True, blank=True)
    PitchingHitByPitch = models.FloatField(null=True, blank=True)
    PitchingSacrifices = models.FloatField(null=True, blank=True)
    PitchingSacrificeFlies = models.FloatField(null=True, blank=True)
    PitchingGroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    PitchingCompleteGames = models.FloatField(null=True, blank=True)
    PitchingShutOuts = models.FloatField(null=True, blank=True)
    PitchingNoHitters = models.FloatField(null=True, blank=True)
    PitchingPerfectGames = models.FloatField(null=True, blank=True)
    PitchingPlateAppearances = models.FloatField(null=True, blank=True)
    PitchingTotalBases = models.FloatField(null=True, blank=True)
    PitchingFlyOuts = models.FloatField(null=True, blank=True)
    PitchingGroundOuts = models.FloatField(null=True, blank=True)
    PitchingLineOuts = models.FloatField(null=True, blank=True)
    PitchingPopOuts = models.FloatField(null=True, blank=True)
    PitchingIntentionalWalks = models.FloatField(null=True, blank=True)
    PitchingReachedOnError = models.FloatField(null=True, blank=True)
    PitchingCatchersInterference = models.FloatField(null=True, blank=True)
    PitchingBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSluggingPercentage = models.FloatField(null=True, blank=True)
    PitchingOnBasePlusSlugging = models.FloatField(null=True, blank=True)
    PitchingStrikeoutsPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingWalksPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingBattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingWeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    DoublePlays = models.FloatField(null=True, blank=True)
    PitchingDoublePlays = models.FloatField(null=True, blank=True)
    BattingOrderConfirmed = models.NullBooleanField()
    IsolatedPower = models.FloatField(null=True, blank=True)
    FieldingIndependentPitching = models.FloatField(null=True, blank=True)
    PitchingQualityStarts = models.FloatField(null=True, blank=True)
    PitchingInningStarted = models.IntegerField(null=True, blank=True)
    LeftOnBase = models.FloatField(null=True, blank=True)
    PitchingHolds = models.FloatField(null=True, blank=True)
    PitchingBlownSaves = models.FloatField(null=True, blank=True)
    SubstituteBattingOrder = models.IntegerField(null=True, blank=True)
    SubstituteBattingOrderSequence = models.IntegerField(null=True, blank=True)
    FantasyPointsFantasyDraft = models.FloatField(null=True, blank=True)

    def get_team(self):
        return self.Team

    def get_name(self):
        return self.Name

    def get_entity_id(self):
        return self.TeamID

    @property
    def vs(self):
        return '%s vs %s' % (self.Team, self.Opponent)

    def __unicode__(self):
        return "{} {}".format(self.vs, self.DateTime)


class TeamGameMLB(models.Model):
    StatID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    GameID = models.IntegerField(null=True, blank=True)
    OpponentID = models.IntegerField(null=True, blank=True)
    Opponent = models.CharField(max_length=10, null=True, blank=True)
    Day = models.DateTimeField(null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    HomeOrAway = models.CharField(max_length=4, null=True, blank=True)
    IsGameOver = models.BooleanField(default=0)
    GlobalGameID = models.IntegerField(null=True, blank=True)
    GlobalOpponentID = models.IntegerField(null=True, blank=True)
    Updated = models.DateTimeField(null=True, blank=True)
    Games = models.IntegerField(null=True, blank=True)
    FantasyPoints = models.FloatField(null=True, blank=True)
    AtBats = models.FloatField(null=True, blank=True)
    Runs = models.FloatField(null=True, blank=True)
    Hits = models.FloatField(null=True, blank=True)
    Singles = models.FloatField(null=True, blank=True)
    Doubles = models.FloatField(null=True, blank=True)
    Triples = models.FloatField(null=True, blank=True)
    HomeRuns = models.FloatField(null=True, blank=True)
    RunsBattedIn = models.FloatField(null=True, blank=True)
    BattingAverage = models.FloatField(null=True, blank=True)
    Outs = models.FloatField(null=True, blank=True)
    Strikeouts = models.FloatField(null=True, blank=True)
    Walks = models.FloatField(null=True, blank=True)
    HitByPitch = models.FloatField(null=True, blank=True)
    Sacrifices = models.FloatField(null=True, blank=True)
    SacrificeFlies = models.FloatField(null=True, blank=True)
    GroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    StolenBases = models.FloatField(null=True, blank=True)
    CaughtStealing = models.FloatField(null=True, blank=True)
    PitchesSeen = models.FloatField(null=True, blank=True)
    OnBasePercentage = models.FloatField(null=True, blank=True)
    SluggingPercentage = models.FloatField(null=True, blank=True)
    OnBasePlusSlugging = models.FloatField(null=True, blank=True)
    Errors = models.FloatField(null=True, blank=True)
    Wins = models.FloatField(null=True, blank=True)
    Losses = models.FloatField(null=True, blank=True)
    Saves = models.FloatField(null=True, blank=True)
    InningsPitchedDecimal = models.FloatField(null=True, blank=True)
    TotalOutsPitched = models.FloatField(null=True, blank=True)
    InningsPitchedFull = models.FloatField(null=True, blank=True)
    InningsPitchedOuts = models.FloatField(null=True, blank=True)
    EarnedRunAverage = models.FloatField(null=True, blank=True)
    PitchingHits = models.FloatField(null=True, blank=True)
    PitchingRuns = models.FloatField(null=True, blank=True)
    PitchingEarnedRuns = models.FloatField(null=True, blank=True)
    PitchingWalks = models.FloatField(null=True, blank=True)
    PitchingStrikeouts = models.FloatField(null=True, blank=True)
    PitchingHomeRuns = models.FloatField(null=True, blank=True)
    PitchesThrown = models.FloatField(null=True, blank=True)
    PitchesThrownStrikes = models.FloatField(null=True, blank=True)
    WalksHitsPerInningsPitched = models.FloatField(null=True, blank=True)
    PitchingBattingAverageAgainst = models.FloatField(null=True, blank=True)
    GrandSlams = models.FloatField(null=True, blank=True)
    FantasyPointsFanDuel = models.FloatField(null=True, blank=True)
    FantasyPointsDraftKings = models.FloatField(null=True, blank=True)
    FantasyPointsYahoo = models.FloatField(null=True, blank=True)
    PlateAppearances = models.FloatField(null=True, blank=True)
    TotalBases = models.FloatField(null=True, blank=True)
    FlyOuts = models.FloatField(null=True, blank=True)
    GroundOuts = models.FloatField(null=True, blank=True)
    LineOuts = models.FloatField(null=True, blank=True)
    PopOuts = models.FloatField(null=True, blank=True)
    IntentionalWalks = models.FloatField(null=True, blank=True)
    ReachedOnError = models.FloatField(null=True, blank=True)
    BallsInPlay = models.FloatField(null=True, blank=True)
    BattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    WeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSingles = models.FloatField(null=True, blank=True)
    PitchingDoubles = models.FloatField(null=True, blank=True)
    PitchingTriples = models.FloatField(null=True, blank=True)
    PitchingGrandSlams = models.FloatField(null=True, blank=True)
    PitchingHitByPitch = models.FloatField(null=True, blank=True)
    PitchingSacrifices = models.FloatField(null=True, blank=True)
    PitchingSacrificeFlies = models.FloatField(null=True, blank=True)
    PitchingGroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    PitchingCompleteGames = models.FloatField(null=True, blank=True)
    PitchingShutOuts = models.FloatField(null=True, blank=True)
    PitchingNoHitters = models.FloatField(null=True, blank=True)
    PitchingPerfectGames = models.FloatField(null=True, blank=True)
    PitchingPlateAppearances = models.FloatField(null=True, blank=True)
    PitchingTotalBases = models.FloatField(null=True, blank=True)
    PitchingFlyOuts = models.FloatField(null=True, blank=True)
    PitchingGroundOuts = models.FloatField(null=True, blank=True)
    PitchingLineOuts = models.FloatField(null=True, blank=True)
    PitchingPopOuts = models.FloatField(null=True, blank=True)
    PitchingIntentionalWalks = models.FloatField(null=True, blank=True)
    PitchingReachedOnError = models.FloatField(null=True, blank=True)
    PitchingCatchersInterference = models.FloatField(null=True, blank=True)
    PitchingBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSluggingPercentage = models.FloatField(null=True, blank=True)
    PitchingOnBasePlusSlugging = models.FloatField(null=True, blank=True)
    PitchingStrikeoutsPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingWalksPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingBattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingWeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    DoublePlays = models.FloatField(null=True, blank=True)
    PitchingDoublePlays = models.FloatField(null=True, blank=True)
    BattingOrderConfirmed = models.NullBooleanField()
    IsolatedPower = models.FloatField(null=True, blank=True)
    FieldingIndependentPitching = models.FloatField(null=True, blank=True)
    PitchingQualityStarts = models.FloatField(null=True, blank=True)
    PitchingInningStarted = models.IntegerField(null=True, blank=True)
    LeftOnBase = models.FloatField(null=True, blank=True)
    PitchingHolds = models.FloatField(null=True, blank=True)
    PitchingBlownSaves = models.FloatField(null=True, blank=True)
    SubstituteBattingOrder = models.IntegerField(null=True, blank=True)
    SubstituteBattingOrderSequence = models.IntegerField(null=True, blank=True)
    FantasyPointsFantasyDraft = models.FloatField(null=True, blank=True)


class PlayerSeasonMLB(models.Model):
    StatID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    PlayerID = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    Position = models.CharField(max_length=10, null=True, blank=True)
    PositionCategory = models.CharField(max_length=10, null=True, blank=True)
    Started = models.IntegerField(null=True, blank=True)
    BattingOrder = models.IntegerField(null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    AverageDraftPosition = models.FloatField(null=True, blank=True)
    Updated = models.DateTimeField(null=True, blank=True)
    Games = models.IntegerField(null=True, blank=True)
    FantasyPoints = models.FloatField(null=True, blank=True)
    AtBats = models.FloatField(null=True, blank=True)
    Runs = models.FloatField(null=True, blank=True)
    Hits = models.FloatField(null=True, blank=True)
    Singles = models.FloatField(null=True, blank=True)
    Doubles = models.FloatField(null=True, blank=True)
    Triples = models.FloatField(null=True, blank=True)
    HomeRuns = models.FloatField(null=True, blank=True)
    RunsBattedIn = models.FloatField(null=True, blank=True)
    BattingAverage = models.FloatField(null=True, blank=True)
    Outs = models.FloatField(null=True, blank=True)
    Strikeouts = models.FloatField(null=True, blank=True)
    Walks = models.FloatField(null=True, blank=True)
    HitByPitch = models.FloatField(null=True, blank=True)
    Sacrifices = models.FloatField(null=True, blank=True)
    SacrificeFlies = models.FloatField(null=True, blank=True)
    GroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    StolenBases = models.FloatField(null=True, blank=True)
    CaughtStealing = models.FloatField(null=True, blank=True)
    PitchesSeen = models.FloatField(null=True, blank=True)
    OnBasePercentage = models.FloatField(null=True, blank=True)
    SluggingPercentage = models.FloatField(null=True, blank=True)
    OnBasePlusSlugging = models.FloatField(null=True, blank=True)
    Errors = models.FloatField(null=True, blank=True)
    Wins = models.FloatField(null=True, blank=True)
    Losses = models.FloatField(null=True, blank=True)
    Saves = models.FloatField(null=True, blank=True)
    InningsPitchedDecimal = models.FloatField(null=True, blank=True)
    TotalOutsPitched = models.FloatField(null=True, blank=True)
    InningsPitchedFull = models.FloatField(null=True, blank=True)
    InningsPitchedOuts = models.FloatField(null=True, blank=True)
    EarnedRunAverage = models.FloatField(null=True, blank=True)
    PitchingHits = models.FloatField(null=True, blank=True)
    PitchingRuns = models.FloatField(null=True, blank=True)
    PitchingEarnedRuns = models.FloatField(null=True, blank=True)
    PitchingWalks = models.FloatField(null=True, blank=True)
    PitchingStrikeouts = models.FloatField(null=True, blank=True)
    PitchingHomeRuns = models.FloatField(null=True, blank=True)
    PitchesThrown = models.FloatField(null=True, blank=True)
    PitchesThrownStrikes = models.FloatField(null=True, blank=True)
    WalksHitsPerInningsPitched = models.FloatField(null=True, blank=True)
    PitchingBattingAverageAgainst = models.FloatField(null=True, blank=True)
    GrandSlams = models.FloatField(null=True, blank=True)
    FantasyPointsFanDuel = models.FloatField(null=True, blank=True)
    FantasyPointsDraftKings = models.FloatField(null=True, blank=True)
    FantasyPointsYahoo = models.FloatField(null=True, blank=True)
    PlateAppearances = models.FloatField(null=True, blank=True)
    TotalBases = models.FloatField(null=True, blank=True)
    FlyOuts = models.FloatField(null=True, blank=True)
    GroundOuts = models.FloatField(null=True, blank=True)
    LineOuts = models.FloatField(null=True, blank=True)
    PopOuts = models.FloatField(null=True, blank=True)
    IntentionalWalks = models.FloatField(null=True, blank=True)
    ReachedOnError = models.FloatField(null=True, blank=True)
    BallsInPlay = models.FloatField(null=True, blank=True)
    BattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    WeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSingles = models.FloatField(null=True, blank=True)
    PitchingDoubles = models.FloatField(null=True, blank=True)
    PitchingTriples = models.FloatField(null=True, blank=True)
    PitchingGrandSlams = models.FloatField(null=True, blank=True)
    PitchingHitByPitch = models.FloatField(null=True, blank=True)
    PitchingSacrifices = models.FloatField(null=True, blank=True)
    PitchingSacrificeFlies = models.FloatField(null=True, blank=True)
    PitchingGroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    PitchingCompleteGames = models.FloatField(null=True, blank=True)
    PitchingShutOuts = models.FloatField(null=True, blank=True)
    PitchingNoHitters = models.FloatField(null=True, blank=True)
    PitchingPerfectGames = models.FloatField(null=True, blank=True)
    PitchingPlateAppearances = models.FloatField(null=True, blank=True)
    PitchingTotalBases = models.FloatField(null=True, blank=True)
    PitchingFlyOuts = models.FloatField(null=True, blank=True)
    PitchingGroundOuts = models.FloatField(null=True, blank=True)
    PitchingLineOuts = models.FloatField(null=True, blank=True)
    PitchingPopOuts = models.FloatField(null=True, blank=True)
    PitchingIntentionalWalks = models.FloatField(null=True, blank=True)
    PitchingReachedOnError = models.FloatField(null=True, blank=True)
    PitchingCatchersInterference = models.FloatField(null=True, blank=True)
    PitchingBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSluggingPercentage = models.FloatField(null=True, blank=True)
    PitchingOnBasePlusSlugging = models.FloatField(null=True, blank=True)
    PitchingStrikeoutsPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingWalksPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingBattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingWeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    DoublePlays = models.FloatField(null=True, blank=True)
    PitchingDoublePlays = models.FloatField(null=True, blank=True)
    BattingOrderConfirmed = models.BooleanField(default=0)
    IsolatedPower = models.FloatField(null=True, blank=True)
    FieldingIndependentPitching = models.FloatField(null=True, blank=True)
    PitchingQualityStarts = models.FloatField(null=True, blank=True)
    PitchingInningStarted = models.IntegerField(null=True, blank=True)
    LeftOnBase = models.FloatField(null=True, blank=True)
    PitchingHolds = models.FloatField(null=True, blank=True)
    PitchingBlownSaves = models.FloatField(null=True, blank=True)
    SubstituteBattingOrder = models.IntegerField(null=True, blank=True)
    SubstituteBattingOrderSequence = models.IntegerField(null=True, blank=True)
    FantasyPointsFantasyDraft = models.FloatField(null=True, blank=True)


class TeamSeasonMLB(models.Model):
    StatID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    Updated = models.DateTimeField(null=True, blank=True)
    Games = models.IntegerField(null=True, blank=True)
    FantasyPoints = models.FloatField(null=True, blank=True)
    AtBats = models.FloatField(null=True, blank=True)
    Runs = models.FloatField(null=True, blank=True)
    Hits = models.FloatField(null=True, blank=True)
    Singles = models.FloatField(null=True, blank=True)
    Doubles = models.FloatField(null=True, blank=True)
    Triples = models.FloatField(null=True, blank=True)
    HomeRuns = models.FloatField(null=True, blank=True)
    RunsBattedIn = models.FloatField(null=True, blank=True)
    BattingAverage = models.FloatField(null=True, blank=True)
    Outs = models.FloatField(null=True, blank=True)
    Strikeouts = models.FloatField(null=True, blank=True)
    Walks = models.FloatField(null=True, blank=True)
    HitByPitch = models.FloatField(null=True, blank=True)
    Sacrifices = models.FloatField(null=True, blank=True)
    SacrificeFlies = models.FloatField(null=True, blank=True)
    GroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    StolenBases = models.FloatField(null=True, blank=True)
    CaughtStealing = models.FloatField(null=True, blank=True)
    PitchesSeen = models.FloatField(null=True, blank=True)
    OnBasePercentage = models.FloatField(null=True, blank=True)
    SluggingPercentage = models.FloatField(null=True, blank=True)
    OnBasePlusSlugging = models.FloatField(null=True, blank=True)
    Errors = models.FloatField(null=True, blank=True)
    Wins = models.FloatField(null=True, blank=True)
    Losses = models.FloatField(null=True, blank=True)
    Saves = models.FloatField(null=True, blank=True)
    InningsPitchedDecimal = models.FloatField(null=True, blank=True)
    TotalOutsPitched = models.FloatField(null=True, blank=True)
    InningsPitchedFull = models.FloatField(null=True, blank=True)
    InningsPitchedOuts = models.FloatField(null=True, blank=True)
    EarnedRunAverage = models.FloatField(null=True, blank=True)
    PitchingHits = models.FloatField(null=True, blank=True)
    PitchingRuns = models.FloatField(null=True, blank=True)
    PitchingEarnedRuns = models.FloatField(null=True, blank=True)
    PitchingWalks = models.FloatField(null=True, blank=True)
    PitchingStrikeouts = models.FloatField(null=True, blank=True)
    PitchingHomeRuns = models.FloatField(null=True, blank=True)
    PitchesThrown = models.FloatField(null=True, blank=True)
    PitchesThrownStrikes = models.FloatField(null=True, blank=True)
    WalksHitsPerInningsPitched = models.FloatField(null=True, blank=True)
    PitchingBattingAverageAgainst = models.FloatField(null=True, blank=True)
    GrandSlams = models.FloatField(null=True, blank=True)
    FantasyPointsFanDuel = models.FloatField(null=True, blank=True)
    FantasyPointsDraftKings = models.FloatField(null=True, blank=True)
    FantasyPointsYahoo = models.FloatField(null=True, blank=True)
    PlateAppearances = models.FloatField(null=True, blank=True)
    TotalBases = models.FloatField(null=True, blank=True)
    FlyOuts = models.FloatField(null=True, blank=True)
    GroundOuts = models.FloatField(null=True, blank=True)
    LineOuts = models.FloatField(null=True, blank=True)
    PopOuts = models.FloatField(null=True, blank=True)
    IntentionalWalks = models.FloatField(null=True, blank=True)
    ReachedOnError = models.FloatField(null=True, blank=True)
    BallsInPlay = models.FloatField(null=True, blank=True)
    BattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    WeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSingles = models.FloatField(null=True, blank=True)
    PitchingDoubles = models.FloatField(null=True, blank=True)
    PitchingTriples = models.FloatField(null=True, blank=True)
    PitchingGrandSlams = models.FloatField(null=True, blank=True)
    PitchingHitByPitch = models.FloatField(null=True, blank=True)
    PitchingSacrifices = models.FloatField(null=True, blank=True)
    PitchingSacrificeFlies = models.FloatField(null=True, blank=True)
    PitchingGroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    PitchingCompleteGames = models.FloatField(null=True, blank=True)
    PitchingShutOuts = models.FloatField(null=True, blank=True)
    PitchingNoHitters = models.FloatField(null=True, blank=True)
    PitchingPerfectGames = models.FloatField(null=True, blank=True)
    PitchingPlateAppearances = models.FloatField(null=True, blank=True)
    PitchingTotalBases = models.FloatField(null=True, blank=True)
    PitchingFlyOuts = models.FloatField(null=True, blank=True)
    PitchingGroundOuts = models.FloatField(null=True, blank=True)
    PitchingLineOuts = models.FloatField(null=True, blank=True)
    PitchingPopOuts = models.FloatField(null=True, blank=True)
    PitchingIntentionalWalks = models.FloatField(null=True, blank=True)
    PitchingReachedOnError = models.FloatField(null=True, blank=True)
    PitchingCatchersInterference = models.FloatField(null=True, blank=True)
    PitchingBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSluggingPercentage = models.FloatField(null=True, blank=True)
    PitchingOnBasePlusSlugging = models.FloatField(null=True, blank=True)
    PitchingStrikeoutsPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingWalksPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingBattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingWeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    DoublePlays = models.FloatField(null=True, blank=True)
    PitchingDoublePlays = models.FloatField(null=True, blank=True)
    BattingOrderConfirmed = models.BooleanField(default=0)
    IsolatedPower = models.FloatField(null=True, blank=True)
    FieldingIndependentPitching = models.FloatField(null=True, blank=True)
    PitchingQualityStarts = models.FloatField(null=True, blank=True)
    PitchingInningStarted = models.IntegerField(null=True, blank=True)
    LeftOnBase = models.FloatField(null=True, blank=True)
    PitchingHolds = models.FloatField(null=True, blank=True)
    PitchingBlownSaves = models.FloatField(null=True, blank=True)
    SubstituteBattingOrder = models.IntegerField(null=True, blank=True)
    SubstituteBattingOrderSequence = models.IntegerField(null=True, blank=True)
    FantasyPointsFantasyDraft = models.FloatField(null=True, blank=True)


class NewsMLB(models.Model):
    NewsID = models.IntegerField(null=True, blank=True)
    Source = models.CharField(max_length=50, null=True, blank=True)
    Updated = models.DateTimeField(null=True, blank=True)
    TimeAgo = models.CharField(max_length=50, null=True, blank=True)
    Title = models.CharField(max_length=100, null=True, blank=True)
    Content = models.CharField(max_length=5000, null=True, blank=True)
    Url = models.CharField(max_length=250, null=True, blank=True)
    TermsOfUse = models.CharField(max_length=500, null=True, blank=True)
    Author = models.CharField(max_length=50, null=True, blank=True)
    Categories = models.CharField(max_length=100, null=True, blank=True)
    PlayerID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    PlayerID2 = models.IntegerField(null=True, blank=True)
    TeamID2 = models.IntegerField(null=True, blank=True)
    Team2 = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return self.Title


class PlayerGameProjectionMLB(models.Model):
    @property
    def locked(self):
        return locked(self.GameID)

    StatID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    PlayerID = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    Position = models.CharField(max_length=10, null=True, blank=True)
    PositionCategory = models.CharField(max_length=10, null=True, blank=True)
    Started = models.IntegerField(null=True, blank=True)
    BattingOrder = models.IntegerField(null=True, blank=True)
    FanDuelSalary = models.IntegerField(null=True, blank=True)
    DraftKingsSalary = models.IntegerField(null=True, blank=True)
    FantasyDataSalary = models.IntegerField(null=True, blank=True)
    YahooSalary = models.IntegerField(null=True, blank=True)
    InjuryStatus = models.CharField(max_length=50, null=True, blank=True)
    InjuryBodyPart = models.CharField(max_length=50, null=True, blank=True)
    InjuryStartDate = models.DateTimeField(null=True, blank=True)
    InjuryNotes = models.CharField(max_length=250, null=True, blank=True)
    FanDuelPosition = models.CharField(max_length=10, null=True, blank=True)
    DraftKingsPosition = models.CharField(max_length=10, null=True, blank=True)
    YahooPosition = models.CharField(max_length=10, null=True, blank=True)
    OpponentRank = models.IntegerField(null=True, blank=True)
    OpponentPositionRank = models.IntegerField(null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    FantasyDraftSalary = models.IntegerField(null=True, blank=True)
    FantasyDraftPosition = models.CharField(max_length=10, null=True, blank=True)
    GameID = models.IntegerField(null=True, blank=True)
    OpponentID = models.IntegerField(null=True, blank=True)
    Opponent = models.CharField(max_length=10, null=True, blank=True)
    Day = models.DateTimeField(null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    HomeOrAway = models.CharField(max_length=4, null=True, blank=True)
    IsGameOver = models.BooleanField(default=0)
    GlobalGameID = models.IntegerField(null=True, blank=True)
    GlobalOpponentID = models.IntegerField(null=True, blank=True)
    Updated = models.DateTimeField(null=True, blank=True)
    Games = models.IntegerField(null=True, blank=True)
    FantasyPoints = models.FloatField(null=True, blank=True)
    AtBats = models.FloatField(null=True, blank=True)
    Runs = models.FloatField(null=True, blank=True)
    Hits = models.FloatField(null=True, blank=True)
    Singles = models.FloatField(null=True, blank=True)
    Doubles = models.FloatField(null=True, blank=True)
    Triples = models.FloatField(null=True, blank=True)
    HomeRuns = models.FloatField(null=True, blank=True)
    RunsBattedIn = models.FloatField(null=True, blank=True)
    BattingAverage = models.FloatField(null=True, blank=True)
    Outs = models.FloatField(null=True, blank=True)
    Strikeouts = models.FloatField(null=True, blank=True)
    Walks = models.FloatField(null=True, blank=True)
    HitByPitch = models.FloatField(null=True, blank=True)
    Sacrifices = models.FloatField(null=True, blank=True)
    SacrificeFlies = models.FloatField(null=True, blank=True)
    GroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    StolenBases = models.FloatField(null=True, blank=True)
    CaughtStealing = models.FloatField(null=True, blank=True)
    PitchesSeen = models.FloatField(null=True, blank=True)
    OnBasePercentage = models.FloatField(null=True, blank=True)
    SluggingPercentage = models.FloatField(null=True, blank=True)
    OnBasePlusSlugging = models.FloatField(null=True, blank=True)
    Errors = models.FloatField(null=True, blank=True)
    Wins = models.FloatField(null=True, blank=True)
    Losses = models.FloatField(null=True, blank=True)
    Saves = models.FloatField(null=True, blank=True)
    InningsPitchedDecimal = models.FloatField(null=True, blank=True)
    TotalOutsPitched = models.FloatField(null=True, blank=True)
    InningsPitchedFull = models.FloatField(null=True, blank=True)
    InningsPitchedOuts = models.FloatField(null=True, blank=True)
    EarnedRunAverage = models.FloatField(null=True, blank=True)
    PitchingHits = models.FloatField(null=True, blank=True)
    PitchingRuns = models.FloatField(null=True, blank=True)
    PitchingEarnedRuns = models.FloatField(null=True, blank=True)
    PitchingWalks = models.FloatField(null=True, blank=True)
    PitchingStrikeouts = models.FloatField(null=True, blank=True)
    PitchingHomeRuns = models.FloatField(null=True, blank=True)
    PitchesThrown = models.FloatField(null=True, blank=True)
    PitchesThrownStrikes = models.FloatField(null=True, blank=True)
    WalksHitsPerInningsPitched = models.FloatField(null=True, blank=True)
    PitchingBattingAverageAgainst = models.FloatField(null=True, blank=True)
    GrandSlams = models.FloatField(null=True, blank=True)
    FantasyPointsFanDuel = models.FloatField(null=True, blank=True)
    FantasyPointsDraftKings = models.FloatField(null=True, blank=True)
    FantasyPointsYahoo = models.FloatField(null=True, blank=True)
    PlateAppearances = models.FloatField(null=True, blank=True)
    TotalBases = models.FloatField(null=True, blank=True)
    FlyOuts = models.FloatField(null=True, blank=True)
    GroundOuts = models.FloatField(null=True, blank=True)
    LineOuts = models.FloatField(null=True, blank=True)
    PopOuts = models.FloatField(null=True, blank=True)
    IntentionalWalks = models.FloatField(null=True, blank=True)
    ReachedOnError = models.FloatField(null=True, blank=True)
    BallsInPlay = models.FloatField(null=True, blank=True)
    BattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    WeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSingles = models.FloatField(null=True, blank=True)
    PitchingDoubles = models.FloatField(null=True, blank=True)
    PitchingTriples = models.FloatField(null=True, blank=True)
    PitchingGrandSlams = models.FloatField(null=True, blank=True)
    PitchingHitByPitch = models.FloatField(null=True, blank=True)
    PitchingSacrifices = models.FloatField(null=True, blank=True)
    PitchingSacrificeFlies = models.FloatField(null=True, blank=True)
    PitchingGroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    PitchingCompleteGames = models.FloatField(null=True, blank=True)
    PitchingShutOuts = models.FloatField(null=True, blank=True)
    PitchingNoHitters = models.FloatField(null=True, blank=True)
    PitchingPerfectGames = models.FloatField(null=True, blank=True)
    PitchingPlateAppearances = models.FloatField(null=True, blank=True)
    PitchingTotalBases = models.FloatField(null=True, blank=True)
    PitchingFlyOuts = models.FloatField(null=True, blank=True)
    PitchingGroundOuts = models.FloatField(null=True, blank=True)
    PitchingLineOuts = models.FloatField(null=True, blank=True)
    PitchingPopOuts = models.FloatField(null=True, blank=True)
    PitchingIntentionalWalks = models.FloatField(null=True, blank=True)
    PitchingReachedOnError = models.FloatField(null=True, blank=True)
    PitchingCatchersInterference = models.FloatField(null=True, blank=True)
    PitchingBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSluggingPercentage = models.FloatField(null=True, blank=True)
    PitchingOnBasePlusSlugging = models.FloatField(null=True, blank=True)
    PitchingStrikeoutsPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingWalksPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingBattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingWeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    DoublePlays = models.FloatField(null=True, blank=True)
    PitchingDoublePlays = models.FloatField(null=True, blank=True)
    BattingOrderConfirmed = models.BooleanField(default=0)
    IsolatedPower = models.FloatField(null=True, blank=True)
    FieldingIndependentPitching = models.FloatField(null=True, blank=True)
    PitchingQualityStarts = models.FloatField(null=True, blank=True)
    PitchingInningStarted = models.IntegerField(null=True, blank=True)
    LeftOnBase = models.FloatField(null=True, blank=True)
    PitchingHolds = models.FloatField(null=True, blank=True)
    PitchingBlownSaves = models.FloatField(null=True, blank=True)
    SubstituteBattingOrder = models.IntegerField(null=True, blank=True)
    SubstituteBattingOrderSequence = models.IntegerField(null=True, blank=True)
    FantasyPointsFantasyDraft = models.FloatField(null=True, blank=True)

    def get_team(self):
        return self.Team

    def get_name(self):
        return self.Name

    def get_entity_id(self):
        return self.TeamID

    @property
    def vs(self):
        return '%s vs %s' % (self.Team, self.Opponent)

    def __unicode__(self):
        return "{} {}".format(self.vs, self.DateTime)


class PlayerSeasonProjectionMLB(models.Model):
    StatID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    PlayerID = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    Team = models.CharField(max_length=10, null=True, blank=True)
    Position = models.CharField(max_length=10, null=True, blank=True)
    PositionCategory = models.CharField(max_length=10, null=True, blank=True)
    Started = models.IntegerField(null=True, blank=True)
    BattingOrder = models.IntegerField(null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    AverageDraftPosition = models.FloatField(null=True, blank=True)
    Updated = models.DateTimeField(null=True, blank=True)
    Games = models.IntegerField(null=True, blank=True)
    FantasyPoints = models.FloatField(null=True, blank=True)
    AtBats = models.FloatField(null=True, blank=True)
    Runs = models.FloatField(null=True, blank=True)
    Hits = models.FloatField(null=True, blank=True)
    Singles = models.FloatField(null=True, blank=True)
    Doubles = models.FloatField(null=True, blank=True)
    Triples = models.FloatField(null=True, blank=True)
    HomeRuns = models.FloatField(null=True, blank=True)
    RunsBattedIn = models.FloatField(null=True, blank=True)
    BattingAverage = models.FloatField(null=True, blank=True)
    Outs = models.FloatField(null=True, blank=True)
    Strikeouts = models.FloatField(null=True, blank=True)
    Walks = models.FloatField(null=True, blank=True)
    HitByPitch = models.FloatField(null=True, blank=True)
    Sacrifices = models.FloatField(null=True, blank=True)
    SacrificeFlies = models.FloatField(null=True, blank=True)
    GroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    StolenBases = models.FloatField(null=True, blank=True)
    CaughtStealing = models.FloatField(null=True, blank=True)
    PitchesSeen = models.FloatField(null=True, blank=True)
    OnBasePercentage = models.FloatField(null=True, blank=True)
    SluggingPercentage = models.FloatField(null=True, blank=True)
    OnBasePlusSlugging = models.FloatField(null=True, blank=True)
    Errors = models.FloatField(null=True, blank=True)
    Wins = models.FloatField(null=True, blank=True)
    Losses = models.FloatField(null=True, blank=True)
    Saves = models.FloatField(null=True, blank=True)
    InningsPitchedDecimal = models.FloatField(null=True, blank=True)
    TotalOutsPitched = models.FloatField(null=True, blank=True)
    InningsPitchedFull = models.FloatField(null=True, blank=True)
    InningsPitchedOuts = models.FloatField(null=True, blank=True)
    EarnedRunAverage = models.FloatField(null=True, blank=True)
    PitchingHits = models.FloatField(null=True, blank=True)
    PitchingRuns = models.FloatField(null=True, blank=True)
    PitchingEarnedRuns = models.FloatField(null=True, blank=True)
    PitchingWalks = models.FloatField(null=True, blank=True)
    PitchingStrikeouts = models.FloatField(null=True, blank=True)
    PitchingHomeRuns = models.FloatField(null=True, blank=True)
    PitchesThrown = models.FloatField(null=True, blank=True)
    PitchesThrownStrikes = models.FloatField(null=True, blank=True)
    WalksHitsPerInningsPitched = models.FloatField(null=True, blank=True)
    PitchingBattingAverageAgainst = models.FloatField(null=True, blank=True)
    GrandSlams = models.FloatField(null=True, blank=True)
    FantasyPointsFanDuel = models.FloatField(null=True, blank=True)
    FantasyPointsDraftKings = models.FloatField(null=True, blank=True)
    FantasyPointsYahoo = models.FloatField(null=True, blank=True)
    PlateAppearances = models.FloatField(null=True, blank=True)
    TotalBases = models.FloatField(null=True, blank=True)
    FlyOuts = models.FloatField(null=True, blank=True)
    GroundOuts = models.FloatField(null=True, blank=True)
    LineOuts = models.FloatField(null=True, blank=True)
    PopOuts = models.FloatField(null=True, blank=True)
    IntentionalWalks = models.FloatField(null=True, blank=True)
    ReachedOnError = models.FloatField(null=True, blank=True)
    BallsInPlay = models.FloatField(null=True, blank=True)
    BattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    WeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSingles = models.FloatField(null=True, blank=True)
    PitchingDoubles = models.FloatField(null=True, blank=True)
    PitchingTriples = models.FloatField(null=True, blank=True)
    PitchingGrandSlams = models.FloatField(null=True, blank=True)
    PitchingHitByPitch = models.FloatField(null=True, blank=True)
    PitchingSacrifices = models.FloatField(null=True, blank=True)
    PitchingSacrificeFlies = models.FloatField(null=True, blank=True)
    PitchingGroundIntoDoublePlay = models.FloatField(null=True, blank=True)
    PitchingCompleteGames = models.FloatField(null=True, blank=True)
    PitchingShutOuts = models.FloatField(null=True, blank=True)
    PitchingNoHitters = models.FloatField(null=True, blank=True)
    PitchingPerfectGames = models.FloatField(null=True, blank=True)
    PitchingPlateAppearances = models.FloatField(null=True, blank=True)
    PitchingTotalBases = models.FloatField(null=True, blank=True)
    PitchingFlyOuts = models.FloatField(null=True, blank=True)
    PitchingGroundOuts = models.FloatField(null=True, blank=True)
    PitchingLineOuts = models.FloatField(null=True, blank=True)
    PitchingPopOuts = models.FloatField(null=True, blank=True)
    PitchingIntentionalWalks = models.FloatField(null=True, blank=True)
    PitchingReachedOnError = models.FloatField(null=True, blank=True)
    PitchingCatchersInterference = models.FloatField(null=True, blank=True)
    PitchingBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingOnBasePercentage = models.FloatField(null=True, blank=True)
    PitchingSluggingPercentage = models.FloatField(null=True, blank=True)
    PitchingOnBasePlusSlugging = models.FloatField(null=True, blank=True)
    PitchingStrikeoutsPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingWalksPerNineInnings = models.FloatField(null=True, blank=True)
    PitchingBattingAverageOnBallsInPlay = models.FloatField(null=True, blank=True)
    PitchingWeightedOnBasePercentage = models.FloatField(null=True, blank=True)
    DoublePlays = models.FloatField(null=True, blank=True)
    PitchingDoublePlays = models.FloatField(null=True, blank=True)
    BattingOrderConfirmed = models.NullBooleanField()
    IsolatedPower = models.FloatField(null=True, blank=True)
    FieldingIndependentPitching = models.FloatField(null=True, blank=True)
    PitchingQualityStarts = models.FloatField(null=True, blank=True)
    PitchingInningStarted = models.IntegerField(null=True, blank=True)
    LeftOnBase = models.FloatField(null=True, blank=True)
    PitchingHolds = models.FloatField(null=True, blank=True)
    PitchingBlownSaves = models.FloatField(null=True, blank=True)
    SubstituteBattingOrder = models.IntegerField(null=True, blank=True)
    SubstituteBattingOrderSequence = models.IntegerField(null=True, blank=True)
    FantasyPointsFantasyDraft = models.FloatField(null=True, blank=True)


class StandingMLB(models.Model):
    Season = models.IntegerField(null=True, blank=True)
    SeasonType = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    Key = models.CharField(max_length=10, default='')
    City = models.CharField(max_length=50, null=True, blank=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    League = models.CharField(max_length=20, null=True, blank=True)
    Division = models.CharField(max_length=20, null=True, blank=True)
    Wins = models.IntegerField(null=True, blank=True)
    Losses = models.IntegerField(null=True, blank=True)
    Percentage = models.FloatField(null=True, blank=True)
    DivisionWins = models.IntegerField(null=True, blank=True)
    DivisionLosses = models.IntegerField(null=True, blank=True)
    GamesBehind = models.FloatField(null=True, blank=True)
    LastTenGamesWins = models.IntegerField(null=True, blank=True)
    LastTenGamesLosses = models.IntegerField(null=True, blank=True)
    Streak = models.CharField(max_length=10, default='')
    WildCardRank = models.IntegerField(null=True, blank=True)
    WildCardGamesBehind = models.FloatField(null=True, blank=True)
    HomeWins = models.IntegerField(null=True, blank=True)
    HomeLosses = models.IntegerField(null=True, blank=True)
    AwayWins = models.IntegerField(null=True, blank=True)
    AwayLosses = models.IntegerField(null=True, blank=True)
    DayWins = models.IntegerField(null=True, blank=True)
    DayLosses = models.IntegerField(null=True, blank=True)
    NightWins = models.IntegerField(null=True, blank=True)
    NightLosses = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u"{} {}".format(self.Season, self.TeamID)


class DfsSlatePlayerMLB(models.Model):
    SlatePlayerID = models.IntegerField(null=True, blank=True)
    SlateID = models.IntegerField()
    SlateGameID = models.IntegerField(null=True, blank=True)
    PlayerID = models.IntegerField(null=True, blank=True)
    PlayerGameProjectionStatID = models.IntegerField(null=True, blank=True)
    OperatorPlayerID = models.CharField(max_length=50, null=True, blank=True)
    OperatorSlatePlayerID = models.CharField(max_length=50, null=True, blank=True)
    OperatorPlayerName = models.CharField(max_length=50, null=True, blank=True)
    OperatorPosition = models.CharField(max_length=10, null=True, blank=True)
    OperatorSalary = models.IntegerField(null=True, blank=True)
    OperatorRosterSlots = JSONField()
    RemovedByOperator = models.NullBooleanField()

    def __unicode__(self):
        return u"{}".format(self.SlatePlayerID)


class DfsSlateGameMLB(models.Model):
    SlateGameID = models.IntegerField(null=True, blank=True)
    SlateID = models.IntegerField()
    GameID = models.IntegerField(null=True, blank=True)
    OperatorGameID = models.IntegerField(null=True, blank=True)
    RemovedByOperator = models.NullBooleanField()


class DfsSlateMLB(models.Model):
    SlateID = models.IntegerField(null=True, blank=True)
    Operator = models.CharField(max_length=50, null=True, blank=True)
    OperatorSlateID = models.IntegerField(null=True, blank=True)
    OperatorName = models.CharField(max_length=50, null=True, blank=True)
    OperatorDay = models.DateTimeField(null=True, blank=True)
    OperatorStartTime = models.DateTimeField(null=True, blank=True)
    NumberOfGames = models.IntegerField(null=True, blank=True)
    IsMultiDaySlate = models.BooleanField(default=0)
    RemovedByOperator = models.BooleanField(default=0)
    OperatorGameType = models.CharField(max_length=50, null=True, blank=True)
    DfsSlateGames = models.ManyToManyField(DfsSlateGameMLB)
    DfsSlatePlayers = models.ManyToManyField(DfsSlatePlayerMLB)

    def __unicode__(self):
        return u"{} {}".format(self.SlateID, self.Operator)


class InningMLB(models.Model):
    InningID = models.IntegerField(null=True, blank=True)
    GameID = models.IntegerField(unique=True)
    InningNumber = models.IntegerField()
    AwayTeamRuns = models.IntegerField(null=True, blank=True)
    HomeTeamRuns = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u"{}".format(self.InningID)


class BoxScoreMLB(models.Model):
    Game = models.OneToOneField(GameMLB)
    Innings = models.ManyToManyField(InningMLB)
    TeamGames = models.ManyToManyField(TeamGameMLB)
    PlayerGames = models.ManyToManyField(PlayerGameMLB)

    def __unicode__(self):
        return u"{}".format(self.Game.GameID)


class SeriesMLB(models.Model):
    series_start = models.DateTimeField(null=True, blank=True)
    series_end = models.DateTimeField(null=True, blank=True)
    HomeTeam = models.CharField(max_length=10, default='')
    AwayTeam = models.CharField(max_length=10, default='')

    @staticmethod
    def extract_series(query, match_date=None):
        """
        :param query: you can either supply ScheduleMLB instance or team name to this parameter
        :param match_date: accepted datetime argument only. defaulted to current date
        :return:
        """
        session = None
        try:
            if not match_date:
                match_date = timezone.now()
            if isinstance(query, ScheduleMLB):
                session = SeriesMLB.objects.get(HomeTeam=query.HomeTeam, AwayTeam=query.AwayTeam,
                                                 series_start__lte=query.Day, series_end__gte=query.Day)
            else:
                session = SeriesMLB.objects.get(Q(HomeTeam=query) | Q(AwayTeam=query), series_start__lte=match_date,
                                                 series_end__gte=match_date)
        except:
            print('No session found for this team and specified date. \
            run command <./manage.py generate_mlb_series> to generate mlb sessions')
        return session


class ScheduleMLB(models.Model):
    GameID = models.IntegerField(null=True, blank=True)
    Season = models.IntegerField()
    SeasonType = models.IntegerField()
    Status = models.CharField(max_length=20, null=True, blank=True)
    Day = models.DateTimeField(null=True, blank=True)
    DateTime = models.DateTimeField(null=True, blank=True)
    AwayTeam = models.CharField(max_length=10, default='')
    HomeTeam = models.CharField(max_length=10, default='')
    AwayTeamID = models.IntegerField(null=True, blank=True)
    HomeTeamID = models.IntegerField(null=True, blank=True)
    GlobalTeamID = models.IntegerField(null=True, blank=True)
    RescheduledGameID = models.IntegerField(null=True, blank=True)
    StadiumID = models.IntegerField(null=True, blank=True)
    Channel = models.CharField(max_length=100, null=True, blank=True)
    Inning = models.IntegerField(null=True, blank=True)
    InningHalf = models.CharField(max_length=1, null=True, blank=True)
    AwayTeamRuns = models.IntegerField(null=True, blank=True)
    HomeTeamRuns = models.IntegerField(null=True, blank=True)
    AwayTeamHits = models.IntegerField(null=True, blank=True)
    HomeTeamHits = models.IntegerField(null=True, blank=True)
    AwayTeamErrors = models.IntegerField(null=True, blank=True)
    HomeTeamErrors = models.IntegerField(null=True, blank=True)
    WinningPitcherID = models.IntegerField(null=True, blank=True)
    LosingPitcherID = models.IntegerField(null=True, blank=True)
    SavingPitcherID = models.IntegerField(null=True, blank=True)
    Attendance = models.IntegerField(null=True, blank=True)
    AwayTeamProbablePitcherID = models.IntegerField(null=True, blank=True)
    HomeTeamProbablePitcherID = models.IntegerField(null=True, blank=True)
    Outs = models.IntegerField(null=True, blank=True)
    Balls = models.IntegerField(null=True, blank=True)
    Strikes = models.IntegerField(null=True, blank=True)
    CurrentPitcherID = models.IntegerField(null=True, blank=True)
    CurrentHitterID = models.IntegerField(null=True, blank=True)
    AwayTeamStartingPitcherID = models.IntegerField(null=True, blank=True)
    HomeTeamStartingPitcherID = models.IntegerField(null=True, blank=True)
    CurrentPitchingTeamID = models.IntegerField(null=True, blank=True)
    CurrentHittingTeamID = models.IntegerField(null=True, blank=True)
    PointSpread = models.FloatField(null=True, blank=True)
    OverUnder = models.FloatField(null=True, blank=True)
    AwayTeamMoneyLine = models.IntegerField(null=True, blank=True)
    HomeTeamMoneyLine = models.IntegerField(null=True, blank=True)
    ForecastTempLow = models.IntegerField(null=True, blank=True)
    ForecastTempHigh = models.IntegerField(null=True, blank=True)
    ForecastDescription = models.CharField(max_length=50, null=True, blank=True)
    ForecastWindChill = models.IntegerField(null=True, blank=True)
    ForecastWindSpeed = models.IntegerField(null=True, blank=True)
    ForecastWindDirection = models.IntegerField(null=True, blank=True)
    RescheduledFromGameID = models.IntegerField(null=True, blank=True)
    RunnerOnFirst = models.NullBooleanField()
    RunnerOnSecond = models.NullBooleanField()
    RunnerOnThird = models.NullBooleanField()
    AwayTeamStartingPitcher = models.CharField(max_length=50, null=True, blank=True)
    HomeTeamStartingPitcher = models.CharField(max_length=50, null=True, blank=True)
    CurrentPitcher = models.CharField(max_length=50, null=True, blank=True)
    CurrentHitter = models.CharField(max_length=50, null=True, blank=True)
    WinningPitcher = models.CharField(max_length=50, null=True, blank=True)
    LosingPitcher = models.CharField(max_length=50, null=True, blank=True)
    SavingPitcher = models.CharField(max_length=50, null=True, blank=True)
    DueUpHitterID1 = models.IntegerField(null=True, blank=True)
    DueUpHitterID2 = models.IntegerField(null=True, blank=True)
    DueUpHitterID3 = models.IntegerField(null=True, blank=True)
    GlobalGameID = models.IntegerField(null=True, blank=True)
    GlobalAwayTeamID = models.IntegerField(null=True, blank=True)
    GlobalHomeTeamID = models.IntegerField(null=True, blank=True)
    PointSpreadAwayTeamMoneyLine = models.IntegerField(null=True, blank=True)
    PointSpreadHomeTeamMoneyLine = models.IntegerField(null=True, blank=True)
    LastPlay = models.CharField(max_length=250, null=True, blank=True)
    IsClosed = models.BooleanField(default=0)
    Updated = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u"{} vs. {} - {}".format(self.HomeTeam, self.AwayTeam, self.Day.date())

    @staticmethod
    def extract_series(team1, team2):
        """
        Consider this Schedule, which is filtered to show only Atlanta games, and is ordered by timestamp.
        You will notice that groups of games appear between ATL and another team. These are called "series", because in baseball, three games are played between the two teams and the winner of the series is based on who wins two out of three.
        WE need to change 3pak Sessions to span the duration of a MLB Session. Session starts at date of first game, and session ends at date of last game.
        extract_series method can be used for extract a series b/w 2 teams.
        :param team1:
        :param team2:
        :return:
        """
        schedule = ScheduleMLB.objects.filter(Q())


class CustomerProfile(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    league = models.ForeignKey(League, null=True)
    name = models.CharField(max_length=150, default='')
    happy_name = models.CharField(max_length=150, default='', blank=False)

    color_primary = models.CharField(max_length=30, default='', blank=True,
                                     help_text='header background color')
    color_secondary = models.CharField(max_length=30, default='', blank=True,
                                       help_text='body text color')
    button_font_color = models.CharField(max_length=30, default='#FDFDFD', blank=True,
                                         help_text='button text color (overrides dark/light)')
    color_3 = models.CharField(max_length=30, default='', blank=True,
                               help_text='body background color')
    color_4 = models.CharField(max_length=30, default='', blank=True,
                               help_text='header/body divider color')
    color_5 = models.CharField(max_length=30, default='', blank=True,
                               help_text='background color of total pts column')
    color_6 = models.CharField(max_length=30, default='', blank=True,
                               help_text='subtitle color')
    color_7 = models.CharField(max_length=30, default='', blank=True,
                               help_text='color of second subtitle')

    color_lhb = models.CharField(max_length=30, default='', blank=True,
                                 help_text='left header boarder')
    color_rhb = models.CharField(max_length=30, default='', blank=True,
                                 help_text='right header boarder')
    color_lhb_2 = models.CharField(max_length=30, default='', blank=True,
                                   help_text='left header boarder for second adv')
    color_rhb_2 = models.CharField(max_length=30, default='', blank=True,
                                   help_text='right header boarder for second adv')
    logo_large = models.ImageField(upload_to='customer_assets', blank=True)
    logo_small = models.ImageField(upload_to='customer_assets', blank=True)
    logo2_large = models.ImageField(upload_to='customer_assets', blank=True)
    logo2_small = models.ImageField(upload_to='customer_assets', blank=True)
    header_background = models.ImageField(upload_to='customer_assets',
                                          blank=True)
    header_title = models.CharField(max_length=100, default='', blank=True)
    header_title_2 = models.CharField(max_length=100, default='', blank=True)
    header_title_padding = models.CharField(max_length=20, default='',
                                            blank=True)
    header_title_2_padding = models.CharField(max_length=20, default='',
                                              blank=True)
    subtitle = models.CharField(max_length=100, default='', blank=True)
    subtitle_2 = models.CharField(max_length=100, default='', blank=True,
                                  help_text='')
    footer_text = models.CharField(max_length=100, default='', blank=True)
    page_ad = models.ImageField(upload_to='customer_assets', blank=True)
    page_ad_2 = models.ImageField(upload_to='customer_assets', blank=True)
    page_ad_3 = models.ImageField(upload_to='customer_assets', blank=True)
    page_ad_4 = models.ImageField(upload_to='customer_assets', blank=True)
    page_ad_style = models.CharField(max_length=255, default='', blank=True,
                                     help_text='full-page banner background')

    promo_blurb = models.TextField(blank=True)
    show_quadbox = models.BooleanField(default=False)
    dark_fonts = models.BooleanField(default=False)
    quadbox_img = models.ImageField(upload_to='customer_assets', blank=True)
    min_age_to_play = models.IntegerField(default=18)
    location_required = models.BooleanField(default=False)

    prize_1 = models.ImageField(upload_to='customer_assets', blank=True)
    prize_2 = models.ImageField(upload_to='customer_assets', blank=True)
    prize_3 = models.ImageField(upload_to='customer_assets', blank=True)
    advertisement = models.ImageField(upload_to='customer_assets', blank=True)
    advertisement_2 = models.ImageField(upload_to='customer_assets', blank=True)

    leader_header_advertisement = models.ImageField(upload_to='customer_assets', blank=True)
    leader_header_advertisement_2 = models.ImageField(upload_to='customer_assets', blank=True)

    advertisement_uri = models.URLField(blank=True)
    advertisement_uri_2 = models.URLField(blank=True)
    prize_top_label_1 = models.CharField(max_length=150, default="Top 10%", blank=True)
    prize_top_label_2 = models.CharField(max_length=150, default="Next 40%", blank=True)
    prize_top_label_3 = models.CharField(max_length=150, default="Everyone Else", blank=True)
    prize_label_1 = models.CharField(max_length=150, default="", blank=True)
    prize_label_2 = models.CharField(max_length=150, default="", blank=True)
    prize_label_3 = models.CharField(max_length=150, default="", blank=True)

    def __unicode__(self):
        return self.name


class GEOFence(models.Model):
    name = models.CharField(max_length=40, default='My Fence', null=False, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    enter_msg = models.CharField(max_length=100, default='', null=False, blank=True)
    exit_msg = models.CharField(max_length=100, default='', null=False, blank=True)
    profiles = models.ManyToManyField(CustomerProfile)

    def __unicode__(self):
        return self.name


class Point(models.Model):
    x = models.DecimalField(max_digits=24, decimal_places=15)
    y = models.DecimalField(max_digits=24, decimal_places=15)
    order = models.IntegerField()
    fence = models.ForeignKey(GEOFence)


class FenceState(models.Model):
    user = models.ForeignKey(User, related_name='fenceStates')
    updated = models.DateTimeField(auto_now=True)
    inside = models.BooleanField(default=False)
    fence = models.ForeignKey(GEOFence, related_name='fenceStates'
                              )

    def inside_text(self):
        if self.inside:
            return "inside"
        else:
            return "outside"

    def __unicode__(self):
        return "{}: {} {} << {}".format(self.user.username, self.inside_text(),
                                        self.fence, self.updated)


class Game(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    GameKey = models.IntegerField(default=0)
    Date = models.DateTimeField(blank=True, null=True)
    AwayTeam = models.CharField(max_length=3, default='')
    HomeTeam = models.CharField(max_length=3, default='')
    SeasonType = models.CharField(max_length=1, default='')
    Season = models.CharField(max_length=4, default='')
    Week = models.CharField(max_length=4, default='')
    Stadium = models.CharField(max_length=100, default='', null=True, blank=True)

    @property
    def vs(self):
        return '%s vs %s' % (self.HomeTeam, self.AwayTeam)

    def __unicode__(self):
        return '%s vs %s - %s' % (self.HomeTeam, self.AwayTeam, self.Date)


def get_demo_now(week):
    # For testing until preseason begins use date of Tuesday first week of season
    return datetime(year=2017, month=8, day=3)


class TournamentSpec(models.Model):
    max_players = models.IntegerField(default=0)
    guaranteed_payout = models.IntegerField(default=0)
    description = models.TextField(default="")
    cost = models.IntegerField(unique=False, default=0)
    GameID = models.IntegerField(null=True, blank=True)

    @property
    def friendly_name(self):
        return self.__unicode__

    def __unicode__(self):
        return "${} to play, {} players, ${} payout".format(self.cost, self.max_players, self.guaranteed_payout)


class TournamentPlacement(models.Model):
    place = models.IntegerField(default=0)
    pays = models.IntegerField(default=0)
    spec = models.ForeignKey(TournamentSpec, null=True)

    def __unicode__(self):
        return "{}: Place {} wins ${}".format(self.spec.description, self.place, self.pays)


class MaxPicksException(Exception):
    def err_code(self):
        return 1


class SalaryException(Exception):
    def err_code(self):
        return 2


class TeamUniqueException(Exception):
    def err_code(self):
        return 3


class Badge(models.Model):
    badge_img = models.ImageField(upload_to='customer_assets', blank=True)
    name = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name


class ThreePak(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, null=True)
    GameID = models.IntegerField(null=True, blank=True)
    final_week_1_score = models.FloatField(default=0.0)
    # final_week_2_score = models.FloatField(default=0.0)

    final_points = models.FloatField(default=0.0)
    final_place = models.IntegerField(default=0)
    final_win = models.FloatField(default=0.0)
    ended = models.BooleanField(default=False)
    prize_code = models.CharField(max_length=6, default="00XX00")
    prize_group = models.IntegerField(default=0)
    prize_text = models.CharField(max_length=50, blank=True)
    prize_image = models.ImageField(upload_to='customer_assets', blank=True)

    @property
    def week_1_score_str(self):
        return "{}".format(self.final_week_1_score)

    @property
    def contest(self):
        if self.contest_set.count():
            return self.contest_set.first()
        else:
            return None

    @property
    def final_print_score(self):
        return str(self.final_points)

    @property
    def final_win_str(self):
        return "$%0.2f" % self.final_win

    # week 2 is implied 
    start_week = models.IntegerField(default=0, db_index=True)
    season_type = models.IntegerField(null=True)
    season = models.IntegerField(null=True)

    def get_picks(self):
        return self.pick_set.all()

    def make_pick(self, obj, id):
        player_type = ContentType.objects.get_for_model(PlayerGameProjectionMLB)
        team_type = ContentType.objects.get_for_model(TeamGameMLB)
        obj_type = ContentType.objects.get_for_model(obj)

        assert (obj_type == player_type or obj_type == team_type)
        existing = self.pick_set.filter(threepak_id=id)

        cnt = len(existing)

        # no more than 3
        if cnt > 2:
            raise MaxPicksException(
                "You already made three picks.  You must remove an existing pick before you can add another.")

        # total salary cannot exceed $20K
        if cnt > 0:
            stotal = reduce(operator.add, [x.content_object.FanDuelSalary for x in existing])
            if (stotal + obj.FanDuelSalary > 17000):
                raise SalaryException("This pick would put you over the salary cap of $17,000.")

        # team cannot be represented more than once
        print 'teams'
        print [x.content_object.get_team() for x in existing]
        print 'obj team'
        print obj.get_team()

        obj = Pick.objects.create(threepak=self, content_object=obj, session_week=1)  # 1 is default..

        return obj

    @property
    def session_weeks_str(self):
        return "{}-{}".format(self.start_week, self.start_week + 1)

    def session_weeks(self):
        return (self.start_week, self.start_week + 1)

    def __unicode__(self):
        return "%s > session wks %d and %d" % (self.user.username, self.start_week, self.start_week + 1)

    def week_score(self, week=None):
        if not week:
            week = Thisweek.objects.first().Week

        pset = self.pick_set.filter(session_week=week)
        if len(pset):
            return round(reduce(operator.add, [x.score() for x in pset]), 2)
        else:
            return 0;

    def total_session_score(self):
        # week = Thisweek.objects.first().Week
        if len(self.pick_set.all()):
            # if self.start_week==week:
            #     pickset = self.pick_set.filter(session_week=week)
            # else:
            # pickset = self.pick_set.all()
            pickset = self.pick_set.all()

            if len(pickset):
                return round(reduce(operator.add, [x.score() for x in pickset]), 2)
            else:
                return 0
        else:
            return 0.0

    def is_session_over(self):
        tw = Thisweek.objects.last()
        last_week = self.start_week + 1
        try:
            return Timeframe.objects.get(Week=last_week, Season=2017, SeasonType=tw.SeasonType).HasLastGameEnded
        except:
            # This is more special DEMO logic to be revisited later
            return False

    @property
    def print_score(self):
        return str(self.total_session_score())

    class Meta:
        ordering = ['-final_points']


class StripeToken(models.Model):
    # just logging token for now
    token = models.CharField(max_length=150)
    customer_id = models.CharField(max_length=150, default="")
    recipient_id = models.CharField(max_length=150, default="")
    user = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return "%s > %s" % (self.user.username, self.token)


class StripeCharge(models.Model):
    token = models.ForeignKey(StripeToken)
    charge_id = models.CharField(max_length=150, default="")
    threepak = models.ForeignKey(ThreePak)

    def __unicode__(self):
        return "%s > %s" % (self.threepak, self.charge_id)


class ContestManager(models.Manager):
    def enter_contest(self, spec, threepak):

        if spec == None:
            spec, created = TournamentSpec.objects.get_or_create(
                description="MLB Contest",
                GameID=threepak.GameID
            )

        contests = Contest.objects.filter(
            spec=spec,
            full=False,
            customer=threepak.user.profile.customer,
            GameID=threepak.GameID
        )
        if len(contests):
            # add to existing contest if not full
            contest = contests.first()
            participants = contest.threepaks.count()

            contest.threepaks.add(threepak)
            return contest

        contest = Contest.objects.create(
            spec=spec,
            full=False,
            customer=threepak.user.profile.customer,
            GameID=threepak.GameID
        )
        contest.threepaks.add(threepak)
        return contest


class News(models.Model):
    NewsID = models.IntegerField()
    Updated = models.DateTimeField()
    Title = models.CharField(max_length=200, default='', blank=True)
    Content = models.TextField()
    PlayerID = models.IntegerField(null=True, blank=True)
    TeamID = models.IntegerField(null=True, blank=True)
    Team = models.CharField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return self.Title


class Contest(models.Model):
    full = models.BooleanField(default=False)
    objects = ContestManager()
    spec = models.ForeignKey(TournamentSpec)
    threepaks = models.ManyToManyField(ThreePak)
    customer = models.ForeignKey(CustomerProfile, null=True, blank=False)

    GameID = models.IntegerField(null=True, blank=True)

    # week 2 is implied  - deprecated for MLB
    start_week = models.IntegerField(default=0, db_index=True)
    season_type = models.IntegerField(null=True)
    season = models.IntegerField(null=True)

    # @property
    # def get_season_type(self):
    #     return Timeframe.get_season_string(self.season_type, self.season)  

    # def __unicode__(self):
    #     return "%s contest #%d, Wks %d-%d  (%d entered)" % (
    #     self.customer, self.id, self.nfl_weeks[0], self.nfl_weeks[1], self.threepaks.count())
    def __unicode__(self):
        return "%s contest #%d, (%d entered)" % (
            self.customer, self.id, self.threepaks.count())

    def sorted_by_position(self, company_name=''):
        paks = self.threepaks.all()
        ss = sorted(paks, key=lambda x: x.total_session_score(), reverse=True)

        return ss

    def get_badges(self, user):
        badges = {}
        # repeat user?
        paks = ThreePak.objects.filter(user=user)
        if paks.count() > 1:
            try:
                badges['repeat_user'] = Badge.objects.get(name='repeat_user').badge_img.url
            except:
                pass

        # if you win 3 times bronze trophy,  4 and a silver and 5 a gold. 
        winners = ThreePak.objects.filter(user=user, prize_code__isnull=False).exclude(prize_code='00XX00')
        if winners.count():
            cnt = winners.count()
            if cnt == 1:
                badges['bronze'] = Badge.objects.get(name='bronze').badge_img.url
            elif cnt == 2:
                badges['silver'] = Badge.objects.get(name='silver').badge_img.url
            elif cnt > 2:
                badges['gold'] = Badge.objects.get(name='gold').badge_img.url

        # Has user invited three players (since a date, or not) that joined and who have played?
        invited = Invite.objects.filter(user=user).values_list('address', flat=True)

        if invited:
            # User may have created user with different case
            rinvited = r'(' + '|'.join(invited) + ')'
            accepted = User.objects.filter(email__iregex=rinvited)

            # And have they played?
            played_count = ThreePak.objects.filter(user__in=accepted).count()
            if played_count >= 3:
                badges['challenge_badge'] = Badge.objects.get(name='challenge_badge').badge_img.url

        return badges

    def get_positions(self):
        # from app.views import sunday_games_started

        ss = self.sorted_by_position()
        pack = []
        for idx in range(0, len(ss)):
            pack.append({
                'username': ss[idx].user.username,
                'badges': self.get_badges(ss[idx].user),
                'pak_id': ss[idx].id,
                # 'view_players': sunday_games_started(),
                'user_id': ss[idx].user.id,
                'position': (idx + 1),
                'total pts': ss[idx].total_session_score(),
                # remove from angular app eventually and use underscore version
                'total_pts': ss[idx].total_session_score()
            })
        return pack

    @property
    def entry_fee(self):
        return self.spec.cost

    @property
    def num_players(self):
        return self.threepaks.count()

    # @property
    # def nfl_weeks(self):
    #     start_week = Timeframe.objects.get(SeasonType=self.season_type, Season=self.season, Week=self.start_week)
    #     next = Timeframe.get_next_timeframe(start_week)
    #     if next:
    #         return (self.start_week, next.Week)
    #     else: 
    #         return (self.start_week, None)

    # def nfl_weeks_str(self):
    #     nflweeks = self.nfl_weeks 
    #     return "{}-{}".format(nflweeks[0], nflweeks[1])


# My assumption:
# FanDual fantasy points are good for one week.
# For example, if Tyrod Taylor earns 30.92 points for week 4, and he remains your pick for week 5,
# and he earns 20 points week 5, then your 3pak score will be:
#
# Total fantasy score: 30.92+20= 50.92
#
# Pick needs to be Player, not PlayerGame.  Players need to be filtered for selection by available GAME for
# the week.


class Pick(models.Model):
    # A pick must have a lifetime of a week
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    threepak = models.ForeignKey(ThreePak, null=True)
    # pick a player or team
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    ordinal = models.IntegerField(default=1)
    session_week = models.IntegerField(default=1, db_index=True)

    def score(self):
        try:
            # score = self.content_object.FantasyPointsFanDuel
            playergame = PlayerGameMLB.objects.get(
                GameID=self.content_object.GameID,
                PlayerID=self.content_object.PlayerID
            )

            return playergame.FantasyPointsFanDuel
        except:
            return 0

    def __unicode__(self):
        if self.content_object:
            return "%s > wk [%d] %s" % (self.threepak, self.session_week, self.content_object.get_name())
        else:
            "Content object is none"


class UserCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, null=True)

    def __str__(self):
        return "{0} [{1}]".format(self.user, self.customer)

    @property
    def company_name(self):
        if self.customer:
            return self.customer.name
        return settings.PAK_DEFAULT_CUSTOMERPROFILE


User.profile = property(
    lambda u: UserCompany.objects.get_or_create(user=u)[0])


class Invite(models.Model):
    user = models.ForeignKey(User, related_name='invites')
    created = models.DateTimeField(auto_now=True)
    address = models.CharField('Email Address', max_length=100)

    def __str__(self):
        return "{0} invited by [{1}]".format(self.address, self.user)


@receiver(post_save, sender=Invite)
def send_invite_email(sender, instance=None, created=False, **kwargs):
    if created:
        from .tasks import invite_user
        invite_user(instance.id)
