from django.test import TestCase

from movies.models import Movie
from planets.models import Planet


class TestMovieModel(TestCase):
    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            'name': 'Tatooine',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
        })

        self.empire = Movie.objects.create(**{
            'name': 'El imperio contraataca',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Robert Watts, George Lucas',
            'release_date': '1980-12-05'
        }).planets.add(self.tatooine)

    def test_model_field_label(self) -> None:
        movie = Movie.objects.all().first()

        for label in ('name', 'opening_text', 'director', 'producer', 'release_date',
                      'planets' ,'created_at', 'updated_at'):

            field_label = movie._meta.get_field(label).verbose_name

            if label.__contains__('_'):
                label = label.replace('_', ' ')

            self.assertEqual(field_label, label)
