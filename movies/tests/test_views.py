from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from json import dumps

from movies.models import Movie
from movies.serializers import MovieSerializer


client = APIClient()


class GetMovieTest(APITestCase):

    def setUp(self) -> None:
        self.empire = Movie.objects.create(**{
            'name': 'El imperio contraataca',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Robert Watts, George Lucas',
            'release_date': '1980-12-05'
        })

        self.jedi = Movie.objects.create(**{
            'name': 'El regreso del jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        })

        self.awaken = Movie.objects.create(**{
            'name': 'El despertar de la Fuerza',
            'director': 'J. J. Abrams',
            'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk',
            'release_date': '2015-12-18'
        })

    def test_get_movie_list(self) -> None:
        response = client.get('/api/v1/movie')
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movie_detail(self) -> None:
        response = client.get(f'/api/v1/movie/{self.jedi.pk}')
        movie = Movie.objects.get(pk=self.jedi.pk)
        serializer = MovieSerializer(movie)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateMovieTest(APITestCase):
    def setUp(self) -> None:
        self.payload = {
            'name': 'El regreso del jedi test',
            'director': 'Richard Marquand test',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum test',
            'release_date': '1983-05-25'
        }

    def test_create_movie(self):
        response = client.post(
            path='/api/v1/movie',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateMovieTest(APITestCase):
    def setUp(self) -> None:
        self.jedi = Movie.objects.create(**{
            'name': 'El regreso del jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        })

        self.awaken = Movie.objects.create(**{
            'name': 'El despertar de la Fuerza',
            'director': 'J. J. Abrams',
            'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk',
            'release_date': '2015-12-18'
        })

        self.payload = {
            'name': 'El regreso del jedi test',
            'director': 'Richard Marquand test',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum test',
            'release_date': '1983-05-25'
        }

    def test_update_put_movie(self) -> None:
        response = client.put(
            path=f'/api/v1/movie/{self.jedi.pk}',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_patch_movie(self) -> None:
        response = client.patch(
            path=f'/api/v1/movie/{self.jedi.pk}',
            data=dumps({'name': 'El regreso del jedi test'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteMovieTest(APITestCase):
    def setUp(self) -> None:
        self.jedi = Movie.objects.create(**{
            'name': 'El regreso del jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        })

    def test_delete_movie(self) -> None:
        response = client.delete(f'/api/v1/movie/{self.jedi.pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
