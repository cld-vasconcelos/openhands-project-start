from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Role, Session
from django.utils import timezone
import datetime

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.role = Role.objects.create(name='test_role')

    def test_user_creation(self):
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertFalse(self.user.is_email_verified)
        self.assertFalse(self.user.two_factor_enabled)

    def test_role_assignment(self):
        self.user.roles.add(self.role)
        self.assertEqual(self.user.roles.count(), 1)
        self.assertEqual(self.user.roles.first(), self.role)

class SessionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.session = Session.objects.create(
            user=self.user,
            token='test-token',
            expires_at=timezone.now() + datetime.timedelta(days=1)
        )

    def test_session_creation(self):
        self.assertEqual(self.session.user, self.user)
        self.assertEqual(self.session.token, 'test-token')
        self.assertTrue(self.session.expires_at > timezone.now())
