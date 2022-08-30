from json import loads

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):

    def setUp(self) -> None:
        User.objects.create_user('user@email.com', 'user', 'User', 'M', '12911223344', 'password')

    def test_list_users(self):
        response = self.client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = loads(response.content)
        self.assertEqual(1, len(json))
        user = json[0]
        self.assertEqual('User', user['name'])
        self.assertEqual('user', user['username'])
