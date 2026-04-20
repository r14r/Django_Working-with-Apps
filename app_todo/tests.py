from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import TodoItem

User = get_user_model()


def make_verified_user(username='user', password='S3cur3Pa$$word!'):
    return User.objects.create_user(
        username=username,
        password=password,
        email=f'{username}@example.com',
        email_verified=True,
    )


class TodoListViewTest(TestCase):
    def setUp(self):
        self.user = make_verified_user()
        self.client.force_login(self.user)

    def test_todo_list_loads(self):
        response = self.client.get(reverse('app_todo:list'))
        self.assertEqual(response.status_code, 200)

    def test_todo_list_shows_only_own_todos(self):
        other_user = make_verified_user('other')
        TodoItem.objects.create(user=self.user, title='Mine')
        TodoItem.objects.create(user=other_user, title='Not mine')
        response = self.client.get(reverse('app_todo:list'))
        self.assertContains(response, 'Mine')
        self.assertNotContains(response, 'Not mine')

    def test_unauthenticated_user_redirected(self):
        self.client.logout()
        response = self.client.get(reverse('app_todo:list'))
        self.assertEqual(response.status_code, 302)

    def test_unverified_user_redirected_to_verify(self):
        unverified = User.objects.create_user(username='unverified', password='pass', email_verified=False)
        self.client.force_login(unverified)
        response = self.client.get(reverse('app_todo:list'))
        self.assertRedirects(response, reverse('app_auth:verify_email_pending'))


class TodoCreateViewTest(TestCase):
    def setUp(self):
        self.user = make_verified_user()
        self.client.force_login(self.user)

    def test_create_todo(self):
        response = self.client.post(reverse('app_todo:create'), {
            'title': 'New task',
            'description': 'Details',
            'is_done': False,
        })
        self.assertRedirects(response, reverse('app_todo:list'))
        self.assertTrue(TodoItem.objects.filter(user=self.user, title='New task').exists())

    def test_create_todo_assigns_current_user(self):
        self.client.post(reverse('app_todo:create'), {
            'title': 'Owned task',
            'description': '',
            'is_done': False,
        })
        item = TodoItem.objects.get(title='Owned task')
        self.assertEqual(item.user, self.user)


class TodoUpdateViewTest(TestCase):
    def setUp(self):
        self.user = make_verified_user()
        self.client.force_login(self.user)
        self.item = TodoItem.objects.create(user=self.user, title='Original')

    def test_update_own_todo(self):
        response = self.client.post(
            reverse('app_todo:update', kwargs={'pk': self.item.pk}),
            {'title': 'Updated', 'description': '', 'is_done': False},
        )
        self.assertRedirects(response, reverse('app_todo:list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, 'Updated')

    def test_cannot_update_other_users_todo(self):
        other_user = make_verified_user('other2')
        other_item = TodoItem.objects.create(user=other_user, title='Theirs')
        response = self.client.post(
            reverse('app_todo:update', kwargs={'pk': other_item.pk}),
            {'title': 'Stolen', 'description': '', 'is_done': False},
        )
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    def setUp(self):
        self.user = make_verified_user()
        self.client.force_login(self.user)
        self.item = TodoItem.objects.create(user=self.user, title='To delete')

    def test_delete_own_todo(self):
        response = self.client.post(reverse('app_todo:delete', kwargs={'pk': self.item.pk}))
        self.assertRedirects(response, reverse('app_todo:list'))
        self.assertFalse(TodoItem.objects.filter(pk=self.item.pk).exists())

    def test_cannot_delete_other_users_todo(self):
        other_user = make_verified_user('other3')
        other_item = TodoItem.objects.create(user=other_user, title='Keep this')
        response = self.client.post(reverse('app_todo:delete', kwargs={'pk': other_item.pk}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(TodoItem.objects.filter(pk=other_item.pk).exists())


class TodoToggleViewTest(TestCase):
    def setUp(self):
        self.user = make_verified_user()
        self.client.force_login(self.user)

    def test_toggle_changes_done_status(self):
        item = TodoItem.objects.create(user=self.user, title='Toggle me', is_done=False)
        self.client.get(reverse('app_todo:toggle', kwargs={'pk': item.pk}))
        item.refresh_from_db()
        self.assertTrue(item.is_done)

    def test_toggle_twice_restores_status(self):
        item = TodoItem.objects.create(user=self.user, title='Toggle twice', is_done=False)
        self.client.get(reverse('app_todo:toggle', kwargs={'pk': item.pk}))
        self.client.get(reverse('app_todo:toggle', kwargs={'pk': item.pk}))
        item.refresh_from_db()
        self.assertFalse(item.is_done)


class TodoApiTest(TestCase):
    def setUp(self):
        self.user = make_verified_user('apiuser')
        self.client.force_login(self.user)

    def test_api_list_returns_own_todos(self):
        TodoItem.objects.create(user=self.user, title='API item')
        response = self.client.get('/todos/api/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'API item')

    def test_api_create_todo(self):
        response = self.client.post('/todos/api/', {
            'title': 'Via API',
            'description': '',
            'is_done': False,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(TodoItem.objects.filter(title='Via API', user=self.user).exists())

    def test_api_requires_authentication(self):
        self.client.logout()
        response = self.client.get('/todos/api/')
        self.assertEqual(response.status_code, 403)

    def test_api_requires_verified_email(self):
        unverified = User.objects.create_user(username='apiunverified', password='pass', email_verified=False)
        self.client.force_login(unverified)
        response = self.client.get('/todos/api/')
        self.assertEqual(response.status_code, 403)
