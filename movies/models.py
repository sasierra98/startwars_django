from django.db import models
from django.utils.timezone import now


class Movie(models.Model):
    name = models.CharField(
        max_length=150
    )

    director = models.CharField(
        max_length=150
    )

    producer = models.CharField(
        max_length=150
    )

    release_date = models.DateField()

    created_at = models.DateTimeField(
        default=now
    )

    updated_at = models.DateTimeField(
        default=now
    )

    def __str__(self) -> str:
        return f'{self.id}|{self.name}'
