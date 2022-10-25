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

        self.empire = Movie.objects.create(**{
            'name': 'El imperio contraataca',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Robert Watts, George Lucas',
            'release_date': '1980-12-05'
        }).planets.add(self.tatooine)

        self.luke = People.objects.create(**{
            'name': 'Luke Skywalker',
            'height': '172',
            'mass': '77',
            'hair_color': 'blond',
            'skin_color': 'fair',
            'eye_color': 'blue',
            'birth_year': '19BBY',
            'gender': 'male',
            'home_world': Planet.objects.get(name='Tatooine'),
        }).movies.add(Movie.objects.get(name='El imperio contraataca'))

    def test_model_field_label(self) -> None:
        people = People.objects.all().first()

        for label in ('name', 'height', 'mass', 'hair_color', 'skin_color',
                      'eye_color', 'birth_year', 'gender', 'home_world',
                      'movies', 'created_at', 'updated_at'):

            field_label = people._meta.get_field(label).verbose_name

            if label.__contains__('_'):
                label = label.replace('_', ' ')

            self.assertEqual(field_label, label)
