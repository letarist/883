from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from django.contrib.auth.models import Group

from .models import Notification, User
from mainapp.models import Article, Tag, Category, Comment


class TestAuthUser(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'admin'
    password = '1234'
    newuser = 'newuser'

    def setUp(self) -> None:
        self.category = Category.objects.create(
            title='cat1'
        )
        self.tag = Tag.objects.create(
            title='tag1'
        )

        self.superuser = User.objects.create_superuser(
            username=self.username,
            password=self.password,
        )

        for i in range(3):
            Article.objects.create(
                category=self.category,
                user=self.superuser,
                tag=self.tag,
                title=f'article-{i}',
                short_desc=f"Short desc{i}",
                body=f"Lorem{i}",
                moderated=1,
            )

        self.client = Client()

    def test_login_logout(self):
        response = self.client.get(reverse('mainapp:index'))
        self.assertEqual(response.status_code, self.status_ok)

        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Logout', status_code=self.status_ok)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get(reverse('personal_account:login'))
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)
        response = self.client.get(reverse('mainapp:index'))
        self.assertContains(response, 'Logout', status_code=self.status_ok)

        self.client.logout()
        response = self.client.get(reverse('personal_account:login'))
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)
        response = self.client.get(reverse('mainapp:index'))
        self.assertNotContains(response, 'Logout', status_code=self.status_ok)

    def test_redirect(self):
        article = Article.objects.first()
        response = self.client.post(reverse('rating:like_article', kwargs={'pk': article.pk, }),
                                    **{'HTTP_X_REQUESTED_WITH':
                                           'XMLHttpRequest'})

        self.assertEqual(response.status_code, self.status_redirect)

    def test_urls(self):

        response = self.client.post(reverse('personal_account:user'))

        self.assertEqual(response.status_code, self.status_redirect)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get(reverse('personal_account:user'))
        self.assertEqual(response.status_code, self.status_ok)

        newuser = User.objects.create_superuser(
            username=self.newuser,
            password=self.password,
        )

        response = self.client.get(reverse('personal_account:our_user', kwargs={'pk': newuser.pk, }))
        self.assertEqual(response.status_code, self.status_ok)
