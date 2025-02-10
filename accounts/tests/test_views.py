from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User

class UserViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        self.client.force_authenticate(user=None)
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123',
        }
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_login(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('user-login'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        response = self.client.post(reverse('user-logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
