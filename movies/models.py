from django.db import models
from django.utils.timezone import now

from planets.models import Planet


class Movie(models.Model):
    name = models.CharField(
        max_length=150
    )

    opening_text = models.TextField(
        null=True
    )

    director = models.CharField(
        max_length=150
    )

    producer = models.CharField(
        max_length=150
    )

    release_date = models.DateField()

    planets = models.ManyToManyField(
        to=Planet
    )

    created_at = models.DateTimeField(
        default=now
    )

    updated_at = models.DateTimeField(
        default=now
    )

    def __str__(self) -> str:
        return f'{self.id}|{self.name}'
