from django.test import TestCase

from characters.models import People
from movies.models import Movie
from planets.models import Planet


class TestPeopleModel(TestCase):
    def setUp(self) -> None:
        self.empire = Movie.objects.create(**{
            'name': 'El imperio contraataca',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Robert Watts, George Lucas',
            'release_date': '1980-12-05'
        })

        self.tatooine = Planet.objects.create(**{
            'name': 'Tatooine',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
        }).movies.add(self.empire)

    def test_model_field_label(self) -> None:
        planet = Planet.objects.all().first()

        for label in ('name', 'diameter', 'climate', 'gravity', 'terrain',
                      'population', 'movies', 'created_at', 'updated_at'):

            field_label = planet._meta.get_field(label).verbose_name

            if label.__contains__('_'):
                label = label.replace('_', ' ')

            self.assertEqual(field_label, label)
