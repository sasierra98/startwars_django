from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from json import dumps

from movies.models import Movie
from planets.models import Planet
from planets.serializers import PlanetSerializer

client = APIClient()


class GetPlanetTest(APITestCase):

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

    def test_get_planet_list(self) -> None:
        response = client.get('/api/v1/planet')
        planet = Planet.objects.all()
        serializer = PlanetSerializer(planet, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_planet_detail(self) -> None:
        planet = Planet.objects.get(name='Tatooine')
        response = client.get(f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}')
        serializer = PlanetSerializer(planet)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreatePlanetTest(APITestCase):
    def setUp(self) -> None:
        self.empire = Movie.objects.create(**{
            'name': 'El imperio contraataca',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Robert Watts, George Lucas',
            'release_date': '1980-12-05'
        })

        self.payload = {
            'name': 'Tatooine',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
            'movies': [self.empire.pk]
        }

    def test_create_planet(self):
        response = client.post(
            path='/api/v1/planet',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdatePlanetTest(APITestCase):
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

        self.payload = {
            'name': 'Tatooine test',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
            'movies': [self.empire.pk]
        }

    def test_update_put_planet(self) -> None:
        response = client.put(
            path=f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_patch_planet(self) -> None:
        response = client.patch(
            path=f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}',
            data=dumps({'name': 'Tatooine test'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeletePlanetTest(APITestCase):
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

    def test_delete_movie(self) -> None:
        response = client.delete(f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
