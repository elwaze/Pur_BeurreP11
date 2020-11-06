from django.db import models


class Created(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)


class Updated(models.Model):
    class Meta:
        abstract = True

    updated = models.DateTimeField(auto_now=True)


class Result(Created, Updated):

    class Meta:
        ordering = ('result',)

    result = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.result} ({self.created})'
