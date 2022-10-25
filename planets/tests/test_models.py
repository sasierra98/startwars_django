from django.test import TestCase

from characters.models import People
from movies.models import Movie
from planets.models import Planet


class TestPeopleModel(TestCase):
    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            'name': 'Tatooine',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
        })

    def test_model_field_label(self) -> None:
        planet = Planet.objects.all().first()

        for label in ('name', 'diameter', 'climate', 'gravity', 'terrain',
                      'population', 'created_at', 'updated_at'):

            field_label = planet._meta.get_field(label).verbose_name

            if label.__contains__('_'):
                label = label.replace('_', ' ')

            self.assertEqual(field_label, label)
