import datetime
from django.core.management import call_command
from django.template.loader import render_to_string
from django_cron import CronJobBase, Schedule
from django.utils.html import strip_tags

from frontend.views import send_email
from core.models import Board
from frontend.models import Subscriber
from django.conf import settings

from django.core.mail import get_connection, EmailMultiAlternatives


def send_mass_html_mail(datatuple, fail_silently=False):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = get_connection(fail_silently=fail_silently)
    messages = []
    for item in datatuple:
        subject = item[0]
        text = item[1]
        html = item[2]
        recipient = item[3]
        message = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


class GenerateDaily(CronJobBase):
    RUN_AT_TIMES = ['5:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'core.generate_daily'

    def do(self):
        today = datetime.datetime.today()
        daily = Board.objects.filter(created=today).first()
        if not daily:
            call_command('generate', all=today.strftime('%d.%m.%Y'), count=2)
        daily = Board.objects.filter(created=today).first()
        if daily:
            print('daily')
            ctx = {'today': today.strftime('%d.%m.%Y'), 'url': daily.file.url}
            subscribers = list(Subscriber.objects.filter(email_validated=True, email='cristi@cbsoft.ro').values('email', 'identifier'))
            messages = []
            for email in subscribers:
                ctx['unsubscribe'] = 'https://kids.cbosft.ro/unsubscribe/{}'.format(email['identifier'])
                message = render_to_string('frontend/daily_email.html', ctx)
                text = strip_tags(message)
                msg = EmailMultiAlternatives('Plansa zilei {}'.format(today.strftime('%d.%m.%Y'), text, settings.EMAIL_FROM, [email['email']]))
                msg.attach_alternative(message, "text/html")
                messages.append(msg)
                #send_email('frontend/daily_email.html', 'Plansa zilei {}'.format(today.strftime('%d.%m.%Y')), ctx, email['email'])
            connection = get_connection(fail_silently=False)
            print(connection)
            print(connection.send_messages(messages))
