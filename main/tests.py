from json import loads

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('user@email.com', 'user', 'User', 'M', '12911223344', 'password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.base_uri = '/api/users/'
        self.user_uri = uri = '/api/users/1/'

    def test_list_users(self):
        response = self.client.get(self.base_uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = loads(response.content)
        self.assertEqual(1, len(json))

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
        put_response = self.client.put(self.user_uri, data=data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        get_response = self.client.get(self.user_uri)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        json = loads(get_response.content)
        self.assertEqual(json['birthday'], data['birthday'])
        self.assertEqual(json['name'], data['name'])
        self.assertEqual(json['genre'], data['genre'])

    def test_delete_user(self):
        delete_response = self.client.delete(self.user_uri)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        get_response = self.client.get(self.user_uri)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
