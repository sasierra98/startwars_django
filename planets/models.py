from django.db import models
from django.utils.timezone import now

from movies.models import Movie


class Planet(models.Model):
    name = models.CharField(
        max_length=150
    )

    diameter = models.PositiveIntegerField()

    climate = models.CharField(
        max_length=150
    )

    gravity = models.FloatField()

    terrain = models.CharField(
        max_length=150
    )

    population = models.PositiveIntegerField()

    movies = models.ManyToManyField(
        to=Movie
    )

    created_at = models.DateTimeField(
        default=now
    )

    updated_at = models.DateTimeField(
        default=now
    )

    def __str__(self) -> str:
        return f'{self.id}|{self.name}'
