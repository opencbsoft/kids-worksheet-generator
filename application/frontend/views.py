from django.shortcuts import render
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string

from core.models import Board
from frontend.models import SubscriberValidation, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_email(template, subject, context, to):
    html_content = render_to_string(template_name=template, context=context)
    text_content = strip_tags(template)
    msg = EmailMultiAlternatives(subject, text_content, settings.FROM_EMAIL, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True


def index(request):
    context = {}
    context['boards'] = Board.objects.all()[:6]
    if request.method == 'POST':
        context['result'] = '0'
        subscriber, created = Subscriber.objects.get_or_create(email=request.POST.get('email'))
        if not subscriber.email_validated:
            validation, created = SubscriberValidation.objects.get_or_create(subscriber=subscriber)
            ctx = {'url': 'https://kids.cbsoft.ro/validate/{}'.format(validation.code)}
            send_email('frontend/validate_email.html', 'Confirma adresa ta de email', ctx, validation.subscriber.email)
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
