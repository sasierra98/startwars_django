from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from movies.models import Movie
from movies.serializers import MovieSerializer


class TestAPIMovie(APITestCase):
    client = APIClient()

    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(**{
            'name': 'test name',
            'director': 'test director',
            'producer': 'test producer',
            'release_date': '2022-10-10'
        })

    def test_model_field_label(self):
        movie = Movie.objects.get(pk=1)

        for label in ('name', 'director', 'producer', 'release_date',
                      'created_at', 'updated_at'):

            field_label = movie._meta.get_field(label).verbose_name

            if label.__contains__('_'):
                label = label.replace('_', ' ')

            self.assertEqual(field_label, label)

    def test_list_movie(self) -> None:
        request = self.client.get('/api/v1/movie')

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_movie(self) -> None:
        request = self.client.post('/api/v1/movie', data={
            'name': 'test name',
            'director': 'test director',
            'producer': 'test producer',
            'release_date': '2022-10-10'
        })

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_detail_movie(self) -> None:
        request = self.client.get('/api/v1/movie/1')

        create_movie = Movie.objects.create(
            name='test name',
            director='test director',
            producer='test producer',
            release_date='2022-10-10'
        )

        print(MovieSerializer(instance=create_movie).data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_update_put_movie(self) -> None:
        request = self.client.put('/api/v1/movie/1', data={
            'name': 'test name',
            'director': 'test director',
            'producer': 'test producer',
            'release_date': '2022-10-10'
        })

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_update_patch_movie(self) -> None:
        request = self.client.patch('/api/v1/movie/1', data={
            'name': 'test name'
        })

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_movie(self) -> None:
        request = self.client.delete('/api/v1/movie/1')

        self.assertEqual(request.status_code, status.HTTP_200_OK)