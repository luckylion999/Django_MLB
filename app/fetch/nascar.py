import requests
from django.conf import settings
from django.utils import timezone
from app.models import (
    NascarRacesSchedule,
    NascarSeries,
    League,
    NascarDriver,
    NascarDriverRaceProjection,
)


class Nascar(object):
    base_url = "https://api.fantasydata.net/nascar/v{version}/json/{api}?key={key}"
    api_version = 2

    def call_api(self, api):
        uri = self.base_url.format(version=self.api_version, api=api, key=settings.FANTASY_DATA_KEY)
        print uri
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise Exception(resp.status_code)

        results = resp.json()
        print results
        return results

    def create_races(self):
        results = self.call_api('races/{}'.format(timezone.now().year))
        for result in results:
            obj = self.save_race(result)

    def create_series(self):
        series = self.call_api('series')
        league, created = League.objects.get_or_create(name='NASCAR')
        for s in series:
            s.update({'league': league})
            obj, created = NascarSeries.objects.get_or_create(
                **s
            )

    def create_drivers(self):
        drivers = self.call_api('drivers')

        for driver in drivers:
            print driver

            obj, created = NascarDriver.objects.get_or_create(
                DriverID=driver.get('DriverID'),
                defaults=driver
            )

    def save_driver_race(self, driver):
        driver_obj = NascarDriverRaceProjection.objects.filter(
            DriverID=driver.get('DriverID'),
            RaceID=driver.get('RaceID')
        )
        if not driver_obj.exists():
            NascarDriverRaceProjection.objects.create(**driver)
        else:
            driver_obj.update(**driver)

    def save_race(self, race):
        race_obj = NascarRacesSchedule.objects.filter(
            RaceID=race.get('RaceID')
        )
        if not race_obj.exists():
            NascarRacesSchedule.objects.create(**race)
        else:
            race_obj.update(**race)

    def create_driver_race(self, race_id):
        drivers = self.call_api('DriverRaceProjections/{}'.format(race_id))
        for driver in drivers:
            self.save_driver_race(driver)

    def create_results(self, race_id):
        results = self.call_api('raceresult/{}'.format(race_id))
        self.save_race(results.get('Race'))
        for driver in results.get('DriverRaces', []):
            self.save_driver_race(driver)
