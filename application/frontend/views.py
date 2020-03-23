from django.shortcuts import render
from core.models import Board
from frontend.models import SubscriberValidation, Subscriber


def index(request):
    context = {}
    context['boards'] = Board.objects.all()[:6]
    if request.method == 'POST':
        context['result'] = '0'
        subscriber, created = Subscriber.objects.get_or_create(email=request.POST.get('email'))
        if not subscriber.email_validated:
            validation = SubscriberValidation.objects.get_or_create(subscriber=subscriber)

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
