from django.core.management.base import BaseCommand
from app.models import GameMLB
from app.fetch.mlb import Mlb
from datetime import datetime
import pytz
import os, time, psutil
from django.utils.timezone import localtime


class Command(BaseCommand):
    utc = pytz.UTC

    def clean_prev_process(self):
        my_pid = os.getpid()
        print "my pid is {}".format(my_pid)
        pids = psutil.pids()  # get list of active pids

        for pid in pids:
            if pid != my_pid:
                try:
                    p = psutil.Process(pid)
                    cmdstr = ' '.join(p.cmdline())
                    print cmdstr
                    if cmdstr.find('fetch_mlb_rt_data') > -1:
                        p.kill()
                        print "killed process: {}".format(pid)
                        time.sleep(10)
                # if we can't access command info skip it
                except psutil.AccessDenied:
                    None

    def handle(self, *args, **options):
        self.clean_prev_process()
        while True:
            curr_date = datetime.now()
            Mlb().save_games(date=curr_date.date())
            games = GameMLB.objects.filter(Day=curr_date.date())
            print curr_date
            for game in games:
                print game.GameID
                game_datetime = localtime(game.DateTime).strftime('%Y-%m-%d %H:%M:%S')
                print game_datetime
                current_date = curr_date.replace(tzinfo=self.utc).strftime('%Y-%m-%d %H:%M:%S')
                print current_date
                game_started = current_date > game_datetime
                print game_started
                if game_started:
                    is_game_pending = game.Status not in ('Final', 'Postponed', 'Canceled')
                    if is_game_pending:
                        print "getting Real Time Data... .. .. . . ."
                        Mlb().save_box_scores(date=curr_date.date())
                        time.sleep(5)

            time.sleep(60)








