import uuid
from django.db import models


class Subscriber(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    email_validated = models.BooleanField(default=False)
    identifier = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.email


class SubscriberValidation(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return str(self.code)
