from django.db import models
from django.utils.timezone import now


class Planet(models.Model):
    name = models.CharField(
        max_length=150
    )

    diameter = models.PositiveBigIntegerField()

    climate = models.CharField(
        max_length=150
    )

    gravity = models.FloatField()

    terrain = models.CharField(
        max_length=150
    )

    population = models.PositiveBigIntegerField()

    created_at = models.DateTimeField(
        default=now
    )

    updated_at = models.DateTimeField(
        default=now
    )

    def clean(self):
        self.updated_at = now()

    def __str__(self) -> str:
        return f'{self.id}|{self.name}'
