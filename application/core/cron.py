import datetime
from django.core.management import call_command
from django_cron import CronJobBase, Schedule

from frontend.views import send_email
from core.models import Board
from frontend.models import Subscriber


class GenerateDaily(CronJobBase):
    RUN_AT_TIMES = ['7:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.generate_daily'

    def do(self):
        today = datetime.datetime.today()
        call_command('generate', all=today.strftime('%d.%m.%Y'), count=2)
        daily = Board.objects.filter(created=today).first()
        if daily:
            ctx = {'today': today.strftime('%d.%m.%Y'), 'url': daily.file.url}
            subscribers = list(Subscriber.objects.filter(email_validated=True).values('email', 'identifier'))
            for email in subscribers:
                ctx['unsubscribe'] = 'https://kids.cbosft.ro/unsubscribe/{}'.format(email['identifier'])
                send_email('frontend/daily_email.html', 'Plansa zilei {}'.format(today.strftime('%d.%m.%Y')), ctx, email['email'])
