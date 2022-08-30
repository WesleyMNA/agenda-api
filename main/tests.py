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

    def test_list_users(self):
        response = self.client.get('/api/users/', format='json')
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
        response = self.client.post('/api/users/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
