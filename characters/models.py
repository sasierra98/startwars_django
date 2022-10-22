from django.db import models
from django.utils.timezone import now

from movies.models import Movie
from planets.models import Planet


class People(models.Model):
    name = models.CharField(
        max_length=150
    )

    height = models.PositiveIntegerField()

    mass = models.PositiveIntegerField()

    hair_color = models.CharField(
        max_length=150
    )

    skin_color = models.CharField(
        max_length=150
    )

    eye_color = models.CharField(
        max_length=150
    )

    birth_year = models.DateField()

    gender = models.CharField(
        max_length=10
    )

    home_world = models.ForeignKey(
        to=Planet,
        on_delete=models.CASCADE
    )

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
