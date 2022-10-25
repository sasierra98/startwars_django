from django.test import TestCase

from movies.models import Movie


class TestMovieModel(TestCase):
    def setUp(self) -> None:
        self.empire = Movie.objects.create(**{
            'name': 'El imperio contraataca',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Robert Watts, George Lucas',
            'release_date': '1980-12-05'
        })

    def test_model_field_label(self) -> None:
        movie = Movie.objects.all().first()

        for label in ('name', 'director', 'producer', 'release_date',
                      'created_at', 'updated_at'):

            field_label = movie._meta.get_field(label).verbose_name

            if label.__contains__('_'):
                label = label.replace('_', ' ')

            self.assertEqual(field_label, label)
