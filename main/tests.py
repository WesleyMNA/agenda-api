from datetime import timedelta
from json import loads

from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User, Event


class BaseTestsSetUp(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('user@email.com',
                                             'user',
                                             'User',
                                             'M',
                                             '12911223344',
                                             'password')
        User.objects.create_user('delete.user@email.com',
                                 'delete.user',
                                 'Delete User',
                                 'M',
                                 '12955667788',
                                 'password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


class EventTests(BaseTestsSetUp):

    def setUp(self) -> None:
        super().setUp()
        Event.objects.create(title='Dentist',
                             description=None,
                             initial_date='2022-01-01 14:00:00+03:00',
                             final_date='2022-01-01 15:00:00+03:00',
                             all_day=False,
                             user=self.user)
        self.base_uri = '/api/events/'

    def test_list_events(self):
        response = self.client.get(self.base_uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = loads(response.content)
        self.assertEqual(1, len(json))

    def test_create_event(self):
        initial_date = timezone.now() + timedelta(hours=1)
        final_date = initial_date + timedelta(hours=1)
        data = {
            'title': 'Gym',
            'description': 'Start at the gym',
            'initial_date': initial_date,
            'final_date': final_date,
            'all_day': False,
            'user': 1
        }
        response = self.client.post(self.base_uri, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_not_create_with_initial_date_before_now(self):
        initial_date = timezone.now() - timedelta(hours=1)
        data = {
            'title': 'Gym',
            'description': 'Start at the gym',
            'initial_date': initial_date,
            'final_date': None,
            'all_day': True,
            'user': 1
        }
        response = self.client.post(self.base_uri, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_create_without_final_date_and_all_day_false(self):
        initial_date = timezone.now() + timedelta(hours=1)
        data = {
            'title': 'Gym',
            'description': 'Start at the gym',
            'initial_date': initial_date,
            'final_date': None,
            'all_day': False,
            'user': 1
        }
        response = self.client.post(self.base_uri, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserTests(BaseTestsSetUp):

    def setUp(self) -> None:
        super().setUp()
        self.base_uri = '/api/users/'

    def test_list_users(self):
        response = self.client.get(self.base_uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = loads(response.content)
        self.assertEqual(2, len(json))

    def test_create_user(self):
        data = {
            'name': 'New User',
            'username': 'new.user',
            'email': 'new.user@email.com',
            'birthday': None,
            'genre': 'F',
            'phone_number': '12988776655',
            'password': 'strong-password',
            'confirm_password': 'strong-password'
        }
        response = self.client.post(self.base_uri, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_not_create_user_with_repeated_username_email_or_phone_number(self):
        data = {
            'name': 'New User',
            'username': 'user',
            'email': 'user@email.com',
            'birthday': None,
            'genre': 'F',
            'phone_number': '12911223344',
            'password': 'strong-password',
            'confirm_password': 'strong-password'
        }
        response = self.client.post(self.base_uri, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        data = {
            'email': 'user@email.com',
            'username': 'user',
            'phone_number': '12911223344',
            'birthday': '2022-01-01',
            'name': 'User 123',
            'genre': 'F'
        }
        user_uri = '/api/users/1/'
        put_response = self.client.put(user_uri, data=data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        get_response = self.client.get(user_uri)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        json = loads(get_response.content)
        self.assertEqual(json['birthday'], data['birthday'])
        self.assertEqual(json['name'], data['name'])
        self.assertEqual(json['genre'], data['genre'])

    def test_delete_user(self):
        delete_uri = '/api/users/2/'
        delete_response = self.client.delete(delete_uri)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        get_response = self.client.get(delete_uri)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
