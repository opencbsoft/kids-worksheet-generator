from django.shortcuts import render
from core.models import Board
from frontend.models import SubscriberValidation


def index(request):
    context = {}
    context['boards'] = Board.objects.all()[:6]

    return render(request, 'frontend/index.html', context)


def validate_email(request, uuid):
    context = {'result': False}
    validation = SubscriberValidation.objects.filter(uuid=uuid).first()
    if validation:
        context = {'result': True}
        if not validation.subscriber.email_validated:
            validation.subscriber.email_validated = True
            validation.subscriber.save()

    return render(request, 'frontend/validation.html', context)
