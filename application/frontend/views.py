from django.shortcuts import render
from core.models import Board
from frontend.models import SubscriberValidation


def index(request):
    context = {}
    context['boards'] = Board.objects.all()[:6]
    if request.method == 'POST':
        context['result'] = 0

    return render(request, 'frontend/index.html', context)


def validate_email(request, uuid):
    context = {'result': 1}
    validation = SubscriberValidation.objects.filter(uuid=uuid).first()
    if validation:
        context = {'result': 2}
        if not validation.subscriber.email_validated:
            validation.subscriber.email_validated = True
            validation.subscriber.save()

    return render(request, 'frontend/validation.html', context)
