import mock
import json

from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from .nascar_data import (
    RACES,
    SERIES,
    DRIVERS,
    DRIVER_RACES,
    RESULTS
)
from app.fetch.nascar import Nascar
from app.models import (
    NascarRacesSchedule,
    NascarDriver,
    NascarSeries,
    NascarDriverRaceProjection
)


class Response(object):
    def __init__(self, content, status=200):
        self.status_code = 200
        self.content = content

    def json(self):
        return json.loads(self.content)


def mock_urls(url):
    print url
    if 'races' in url:
        data = json.dumps(RACES)
    elif 'series' in url:
        data = json.dumps(SERIES)
    elif 'drivers' in url:
        data = json.dumps(DRIVERS)
    elif 'DriverRaceProjections' in url:
        data = json.dumps(DRIVER_RACES)
    elif 'raceresult' in url:
        data = json.dumps(RESULTS)
    return Response(data)


@mock.patch('requests.get', mock_urls)
class NascarTest(TestCase):
    def setUp(self):
        self.nascar = Nascar()
        self.RaceID = 101

    def test_races(self):
        self.nascar.create_races()
        self.assertEqual(NascarRacesSchedule.objects.count(), len(RACES))

    def test_series(self):
        self.nascar.create_series()
        self.assertEqual(NascarSeries.objects.count(), len(SERIES))

    def test_drivers(self):
        self.nascar.create_drivers()
        self.assertEqual(NascarDriver.objects.count(), len(DRIVERS))

    def test_driver_race(self):
        self.nascar.create_driver_race(self.RaceID)
        self.assertEqual(NascarDriverRaceProjection.objects.count(), len(DRIVER_RACES))

    def test_results(self):
        self.nascar.create_races()
        self.nascar.create_driver_race(self.RaceID)
        self.nascar.create_results(self.RaceID)

        race = NascarRacesSchedule.objects.get(RaceID=self.RaceID)

        for field, value in RESULTS.get('Race').iteritems():
            old_value = getattr(race, field)
            if type(old_value) == datetime:
                old_value = timezone.localtime(old_value).strftime("%Y-%m-%dT%H:%M:%S")
            self.assertEqual(old_value, value)

        driver = NascarDriverRaceProjection.objects.get(DriverID=int(race.WinnerID))
        driver_result = filter(lambda x: x.get('DriverID') == driver.DriverID, RESULTS.get('DriverRaces'))[0]
        for field, value in driver_result.iteritems():
            old_value = getattr(driver, field)
            if type(old_value) == datetime:
                old_value = timezone.localtime(old_value).strftime("%Y-%m-%dT%H:%M:%S")
            self.assertEqual(old_value, value)
