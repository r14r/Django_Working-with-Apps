from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegistrationViewTest(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse('auth_app:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registrieren')

    def test_register_creates_unverified_user(self):
        response = self.client.post(reverse('auth_app:register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'S3cur3Pa$$word!',
            'password2': 'S3cur3Pa$$word!',
        })
        self.assertRedirects(response, reverse('auth_app:verify_email_pending'))
        user = User.objects.get(username='testuser')
        self.assertFalse(user.email_verified)
        self.assertIsNotNone(user.email_verification_token)

    def test_register_sends_verification_email(self):
        from django.core import mail
        self.client.post(reverse('auth_app:register'), {
            'username': 'mailuser',
            'email': 'mail@example.com',
            'password1': 'S3cur3Pa$$word!',
            'password2': 'S3cur3Pa$$word!',
        })
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('mail@example.com', mail.outbox[0].to)

    def test_authenticated_user_redirected_from_register(self):
        user = User.objects.create_user(username='existing', password='pass', email_verified=True)
        self.client.force_login(user)
        response = self.client.get(reverse('auth_app:register'))
        self.assertRedirects(response, reverse('todo:list'))


class EmailVerificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='verifyuser',
            email='verify@example.com',
            password='S3cur3Pa$$word!',
            email_verified=False,
        )

    def test_verify_email_link_activates_account(self):
        token = self.user.email_verification_token
        response = self.client.get(reverse('auth_app:verify_email', kwargs={'token': str(token)}))
        self.assertRedirects(response, reverse('auth_app:login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_verified)

    def test_verify_email_invalid_token_returns_404(self):
        import uuid
        fake_token = uuid.uuid4()
        response = self.client.get(reverse('auth_app:verify_email', kwargs={'token': str(fake_token)}))
        self.assertEqual(response.status_code, 404)

    def test_login_blocked_for_unverified_user(self):
        response = self.client.post(reverse('auth_app:login'), {
            'username': 'verifyuser',
            'password': 'S3cur3Pa$$word!',
        })
        self.assertRedirects(response, reverse('auth_app:verify_email_pending'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_allowed_for_verified_user(self):
        self.user.email_verified = True
        self.user.save()
        response = self.client.post(reverse('auth_app:login'), {
            'username': 'verifyuser',
            'password': 'S3cur3Pa$$word!',
        })
        self.assertRedirects(response, reverse('todo:list'))

    def test_resend_verification_email_sends_mail(self):
        from django.core import mail
        response = self.client.post(reverse('auth_app:resend_verification'), {
            'email': 'verify@example.com',
        })
        self.assertRedirects(response, reverse('auth_app:verify_email_pending'))
        self.assertEqual(len(mail.outbox), 1)


class CustomUserRoleTest(TestCase):
    def test_default_role_is_member(self):
        user = User.objects.create_user(username='roletest', password='pass')
        self.assertEqual(user.role, 'member')

    def test_admin_role_can_be_set(self):
        user = User.objects.create_user(username='adminuser', password='pass', role='admin')
        self.assertEqual(user.role, 'admin')
