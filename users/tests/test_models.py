from django.test import TestCase
from django.utils import timezone
from users.models import User, Role, UserRole, Session, MFA


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_email_verified)
        self.assertFalse(user.two_factor_enabled)


class RoleModelTest(TestCase):
    def test_create_role(self):
        role = Role.objects.create(name='admin')
        self.assertEqual(role.name, 'admin')


class UserRoleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password'
        )
        self.role = Role.objects.create(name='admin')

    def test_assign_role_to_user(self):
        user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.assertEqual(user_role.user, self.user)
        self.assertEqual(user_role.role, self.role)


class SessionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password'
        )

    def test_create_session(self):
        expires_at = timezone.now() + timezone.timedelta(days=1)
        session = Session.objects.create(
            user=self.user,
            token='test_token',
            expires_at=expires_at
        )
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.token, 'test_token')


class MFAModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password'
        )

    def test_create_mfa(self):
        mfa = MFA.objects.create(
            user=self.user,
            secret_key='test_secret'
        )
        self.assertEqual(mfa.user, self.user)
        self.assertEqual(mfa.secret_key, 'test_secret')
