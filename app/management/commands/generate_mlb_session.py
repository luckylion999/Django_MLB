from django.core.management.base import BaseCommand
from app.models import SeriesMLB, ScheduleMLB
from datetime import timedelta
import itertools

import operator


def club_date(cutoff, key=None, predicate=None):
    if key is None:
        key = lambda v: v
    if predicate is None:
        def predicate(lhs, rhs):
            return lhs - cutoff <= rhs <= lhs + cutoff

    class K(object):
        __slots__ = ['obj']

        def __init__(self, obj):
            self.obj = obj

        def __eq__(self, other):
            ret = predicate(key(self.obj), key(other.obj))
            if ret:
                self.obj = other.obj
            return ret

    return K


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--syncall',
                            action='store_true',
                            help='Sync all MLB Session data', )

    def handle(self, *args, **options):
        get_attr = operator.attrgetter('Day')
        if options['syncall']:
            SeriesMLB.objects.all().delete()
            all_teams = ScheduleMLB.objects.values_list('HomeTeam', flat=True).distinct()
            for group in itertools.combinations(all_teams, 2):
                schedules = ScheduleMLB.objects.filter(HomeTeam=group[0], AwayTeam=group[1]).order_by('Day')
                for session in [list(g) for k, g in
                                itertools.groupby(schedules, club_date(timedelta(days=2), key=get_attr))]:
                    SeriesMLB.objects.create(
                        series_start=session[0].Day,
                        series_end=session[-1].Day,
                        HomeTeam=group[0],
                        AwayTeam=group[1]
                    )
        else:
            last_synced_series = SeriesMLB.objects.order_by('-series_start').first()
            query = {}
            if last_synced_series:
                query["Day__gte"] = last_synced_series.series_start
            all_teams = ScheduleMLB.objects.values_list('HomeTeam', flat=True).distinct()
            for group in itertools.combinations(all_teams, 2):
                query["HomeTeam"] = group[0]
                query["AwayTeam"] = group[1]
                schedules = ScheduleMLB.objects.filter(**query).order_by('Day')
                for session in [list(g) for k, g in
                                itertools.groupby(schedules, club_date(timedelta(days=2), key=get_attr))]:
                    try:
                        sobj = SeriesMLB.objects.get(
                            series_start=session[0].Day,
                            HomeTeam=group[0],
                            AwayTeam=group[1]
                        )
                        if sobj.series_end != session[-1].Day:
                            sobj.series_end = session[-1].Day
                            sobj.save()
                    except SeriesMLB.DoesNotExist:
                        SeriesMLB.objects.create(
                            series_start=session[0].Day,
                            series_end=session[-1].Day,
                            HomeTeam=group[0],
                            AwayTeam=group[1]
                        )
