from django_cron import CronJobBase, Schedule


class GenerateDaily(CronJobBase):
    RUN_AT_TIMES = ['9:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.generate_daily'

    def do(self):
        pass
