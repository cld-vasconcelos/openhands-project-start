from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import User, Role, Session

class UserModelTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='test_role')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.roles.add(self.role)

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertFalse(self.user.is_email_verified)
        self.assertFalse(self.user.two_factor_enabled)
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_role_relationship(self):
        self.assertEqual(self.user.roles.count(), 1)
        self.assertEqual(self.user.roles.first(), self.role)

class RoleModelTests(TestCase):
    def test_role_creation(self):
        role = Role.objects.create(name='admin')
        self.assertEqual(str(role), 'admin')

class SessionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.session = Session.objects.create(
            user=self.user,
            token='test_token',
            expires_at=timezone.now() + timedelta(days=1)
        )

    def test_session_creation(self):
        self.assertEqual(self.session.user, self.user)
        self.assertEqual(self.session.token, 'test_token')
        self.assertTrue(self.session.expires_at > timezone.now())
