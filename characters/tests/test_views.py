from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from json import dumps

from characters.serializers import PeopleSerializer
from movies.models import Movie
from planets.models import Planet
from characters.models import People


client = APIClient()


class GetPeopleTest(APITestCase):

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

    def test_get_people_list(self) -> None:
        response = client.get('/api/v1/people')
        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_people_detail(self) -> None:
        people = People.objects.get(name='Luke Skywalker')
        response = client.get(f'/api/v1/people/{people.pk}')
        serializer = PeopleSerializer(people)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreatePeopleTest(APITestCase):
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
            'name': 'Luke Skywalker',
            'height': '172',
            'mass': '77',
            'hair_color': 'blond',
            'skin_color': 'fair',
            'eye_color': 'blue',
            'birth_year': '19BBY',
            'gender': 'male',
            'home_world': Planet.objects.get(name='Tatooine').pk,
            'movies': [Movie.objects.get(name='El imperio contraataca').pk]
        }

    def test_create_people(self):
        response = client.post(
            path='/api/v1/people',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdatePeopleTest(APITestCase):
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
        }).movies.add(self.empire)

        self.payload = {
            'name': 'Luke Skywalker',
            'height': '172',
            'mass': '77',
            'hair_color': 'blond',
            'skin_color': 'fair',
            'eye_color': 'blue',
            'birth_year': '19BBY',
            'gender': 'male',
            'home_world': Planet.objects.get(name='Tatooine').pk,
            'movies': [Movie.objects.get(name='El imperio contraataca').pk]
        }

    def test_update_put_people(self) -> None:
        response = client.put(
            path=f'/api/v1/people/{People.objects.get(name="Luke Skywalker").pk}',
            data=dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_patch_people(self) -> None:
        response = client.patch(
            path=f'/api/v1/people/{People.objects.get(name="Luke Skywalker").pk}',
            data=dumps({'name': 'Luke Skywalker test'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeletePeopleTest(APITestCase):
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
        }).movies.add(self.empire)

    def test_delete_movie(self) -> None:
        response = client.delete(f'/api/v1/people/{People.objects.get(name="Luke Skywalker").pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
