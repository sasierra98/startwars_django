from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from json import dumps

from movies.models import Movie
from movies.serializers import MovieSerializer
from planets.models import Planet

client = APIClient()


class GetMovieTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            "name": "Tatooine",
            "diameter": 10465,
            "climate": "arid",
            "gravity": 1,
            "terrain": "desert",
            "population": 200000
        })

        Movie.objects.create(**{
            'name': 'El imperio contraataca',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Robert Watts, George Lucas',
            'release_date': '1980-12-05'
        }).planets.add(self.tatooine)

        self.jedi = Movie.objects.create(**{
            'name': 'El regreso del jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        }).planets.add(self.tatooine)

        self.awaken = Movie.objects.create(**{
            'name': 'El despertar de la Fuerza',
            'director': 'J. J. Abrams',
            'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk',
            'release_date': '2015-12-18'
        }).planets.add(self.tatooine)

    def test_get_movie_list(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        response = client.get('/api/v1/movie')
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movie_detail(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        response = client.get(f'/api/v1/movie/{Movie.objects.get(name="El imperio contraataca").pk}')
        movie = Movie.objects.get(name="El imperio contraataca")
        serializer = MovieSerializer(movie)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateMovieTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            "name": "Tatooine",
            "diameter": 10465,
            "climate": "arid",
            "gravity": 1,
            "terrain": "desert",
            "population": 200000
        })

        self.payload = {
            'name': 'El regreso del jedi test',
            'opening_text': 'text',
            'director': 'Richard Marquand test',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum test',
            'release_date': '1983-05-25',
            'planets': [Planet.objects.filter(name='Tatooine').last().pk]
        }

    def test_create_movie(self):
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)

        response = client.post(
            path='/api/v1/movie',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateMovieTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            "name": "Tatooine",
            "diameter": 10465,
            "climate": "arid",
            "gravity": 1,
            "terrain": "desert",
            "population": 200000
        })

        Movie.objects.create(**{
            'name': 'El regreso del jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        }).planets.add(self.tatooine)

        self.payload = {
            'name': 'El regreso del jedi test',
            'director': 'Richard Marquand test',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum test',
            'release_date': '1983-05-25',
            'planets': [Planet.objects.get(name='Tatooine').pk]
        }

    def test_update_put_movie(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)

        response = client.put(
            path=f'/api/v1/movie/{Movie.objects.get(name="El regreso del jedi").pk}',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_patch_movie(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)

        response = client.patch(
            path=f'/api/v1/movie/{Movie.objects.get(name="El regreso del jedi").pk}',
            data=dumps({'name': 'El regreso del jedi test'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteMovieTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            "name": "Tatooine",
            "diameter": 10465,
            "climate": "arid",
            "gravity": 1,
            "terrain": "desert",
            "population": 200000
        })

        self.jedi = Movie.objects.create(**{
            'name': 'El regreso del jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        }).planets.add(self.tatooine)

    def test_delete_movie(self) -> None:
        response = client.delete(f'/api/v1/movie/{Movie.objects.get(name="El regreso del jedi").pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
