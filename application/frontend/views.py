from django.shortcuts import render
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string

from core.models import Board
from frontend.models import SubscriberValidation, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email as validate_email_address


def send_email(template, subject, context, to):
    html_content = render_to_string(template_name=template, context=context)
    text_content = strip_tags(template)
    if type(to) is list:
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, bcc=to)
    else:
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True


def index(request):
    context = {'boards': Board.objects.all()[:6]}
    if request.method == 'POST':
        context['result'] = '0'
        if request.POST.get('email'):
            email = request.POST.get('email').lower()
            try:
                validate_email_address(email)
            except:
                context['result'] = '7'
            else:
                subscriber, created = Subscriber.objects.get_or_create(email=email)
                if not subscriber.email_validated:
                    validation, created = SubscriberValidation.objects.get_or_create(subscriber=subscriber)
                    ctx = {'url': 'https://kids.cbsoft.ro/validate/{}'.format(validation.code)}
                    send_email('frontend/validate_email.html', 'Confirma adresa ta de email', ctx, validation.subscriber.email)
    context['abonati'] = Subscriber.objects.count()
    return render(request, 'frontend/index.html', context)


def validate_email(request, uuid):
    context = {'result': '1'}
    validation = SubscriberValidation.objects.filter(code=uuid).first()
    if validation:
        context = {'result': '2'}
        if not validation.subscriber.email_validated:
            validation.subscriber.email_validated = True
            validation.subscriber.save()
        validation.delete()
    context['boards'] = Board.objects.all()[:6]
    return render(request, 'frontend/index.html', context)


def unsubscribe(request, uuid):
    subscriber = Subscriber.objects.filter(identifier=uuid).first()
    if subscriber:
        context = {'result': '3'}
    else:
        context = {'result': '4'}
    if request.method == 'POST':
        if request.POST.get('action', '') == 'unsubscribe':
            subscriber.unsubscribed = True
            subscriber.save()
            context = {'result': '5'}
    context['uuid'] = uuid
    context['boards'] = Board.objects.all()[:6]
    return render(request, 'frontend/index.html', context)
