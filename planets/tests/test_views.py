from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from json import dumps

from movies.models import Movie
from planets.models import Planet
from planets.serializers import PlanetSerializer

client = APIClient()


class GetPlanetTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            'name': 'Tatooine',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
        })

    def test_get_planet_list(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        response = client.get('/api/v1/planet')
        planet = Planet.objects.all()
        serializer = PlanetSerializer(planet, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_planet_detail(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        planet = Planet.objects.get(name='Tatooine')
        response = client.get(f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}')
        serializer = PlanetSerializer(planet)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreatePlanetTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.payload = {
            'name': 'Tatooine',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000
        }

    def test_create_planet(self):
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        response = client.post(
            path='/api/v1/planet',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdatePlanetTest(APITestCase):
    fixtures = ['users.json']

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

        self.payload = {
            'name': 'Tatooine test',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
        }

    def test_update_put_planet(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        response = client.put(
            path=f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_patch_planet(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        response = client.patch(
            path=f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}',
            data=dumps({'name': 'Tatooine test'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeletePlanetTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.tatooine = Planet.objects.create(**{
            'name': 'Tatooine',
            'diameter': 10465,
            'climate': 'arid',
            'gravity': 1,
            'terrain': 'desert',
            'population': 200000,
        })

    def test_delete_planet(self) -> None:
        api_user = User.objects.get(username='developer')

        client.force_authenticate(user=api_user)
        response = client.delete(f'/api/v1/planet/{Planet.objects.get(name="Tatooine").pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
