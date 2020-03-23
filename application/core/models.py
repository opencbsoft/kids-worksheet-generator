from django.db import models


class Board(models.Model):
    created = models.DateField()
    file = models.FileField(upload_to="worksheets")

    def __str__(self):
        return self.file
