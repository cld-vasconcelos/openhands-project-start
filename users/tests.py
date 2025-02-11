from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import User, Role, Session

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.role = Role.objects.create(name='user')

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.is_email_verified)
        self.assertFalse(self.user.two_factor_enabled)

    def test_user_role_relationship(self):
        self.user.roles.add(self.role)
        self.assertEqual(self.user.roles.count(), 1)
        self.assertEqual(self.user.roles.first().name, 'user')

class RoleModelTests(TestCase):
    def test_role_creation(self):
        role = Role.objects.create(name='admin')
        self.assertEqual(str(role), 'admin')
        self.assertTrue(isinstance(role.created_at, timezone.datetime))
        self.assertTrue(isinstance(role.updated_at, timezone.datetime))

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
            expires_at=timezone.now() + timedelta(days=1)
        )

    def test_session_creation(self):
        self.assertEqual(str(self.session), f"{self.user.email} - {self.session.created_at}")
        self.assertEqual(self.session.user, self.user)
        self.assertEqual(self.session.token, 'test-token')
