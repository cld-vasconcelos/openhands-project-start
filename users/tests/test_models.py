import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from users.models import Role, Session
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class TestUserModel(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(**self.user_data)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_user_str(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])

class TestRoleModel(TestCase):
    def test_create_role(self):
        role = Role.objects.create(name='admin')
        self.assertEqual(role.name, 'admin')
        self.assertIsNotNone(role.created_at)
        self.assertIsNotNone(role.updated_at)

    def test_role_str(self):
        role = Role.objects.create(name='moderator')
        self.assertEqual(str(role), 'moderator')

class TestSessionModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.session_data = {
            'user': self.user,
            'token': 'test-token-123',
            'expires_at': timezone.now() + timedelta(days=1)
        }

    def test_create_session(self):
        session = Session.objects.create(**self.session_data)
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.token, self.session_data['token'])
        self.assertIsNotNone(session.created_at)
        self.assertIsNotNone(session.expires_at)

    def test_session_str(self):
        session = Session.objects.create(**self.session_data)
        expected_str = f"{self.user.email} - {session.created_at}"
        self.assertEqual(str(session), expected_str)
