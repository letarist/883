from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from mainapp.models import Category, Article, Tag, Comment
from personal_account.models import User


class TestMainappSmoke(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'django'
    password = 'django'

    def setUp(self) -> None:
        self.category = Category.objects.create(
            title='Разработка'
        )
        for i in range(10):
            Category.objects.create(
                title=f'Title {i}'
            )
        self.tag = Tag.objects.create(
            title='Python'
        )
        self.user = User.objects.create(
            description='description',
            username='user',
            password='user',
            first_name='first name',
            last_name='last name'
        )
        self.article = Article.objects.create(
            category=self.category,
            user=self.user,
            tag=self.tag,
            title='title',
            short_desc='short description',
            body='body',
        )
        self.not_moderated_article = Article.objects.create(
            category=self.category,
            user=self.user,
            tag=self.tag,
            title='not moderated title',
            short_desc='not moderated short description',
            body='not moderated body',
            moderated=0
        )
        for i in range(10):
            Article.objects.create(
                category=self.category,
                user=self.user,
                tag=self.tag,
                title=f'title {i}',
                short_desc=f'short description {i}',
                body=f'body {i}',
                moderated=1
            )
        for i in range(10):
            Article.objects.create(
                category=self.category,
                user=self.user,
                tag=self.tag,
                title=f'not moderated title {i}',
                short_desc=f'not moderated short description {i}',
                body=f'not moderated body {i}',
                moderated=0
            )
        self.comment = Comment.objects.create(
            article=self.article,
            user=self.user,
            body='body'
        )
        for i in range(20):
            Comment.objects.create(
                article=self.article,
                user=self.user,
                body=f'body {i}'
            )
        self.superuser = User.objects.create_superuser(
            description='super description',
            username=self.username,
            password=self.password,
            first_name='super first name',
            last_name='super last name'
        )
        self.user_moder = User.objects.create(
            description='moder description',
            username='moderuser',
            password='moderuser',
            first_name='moder first name',
            last_name='moder last name',
            is_moder=True
        )
        self.client = Client()

    def test_mainapp_url(self):
        """test if main page and page help are opened"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/help/')
        self.assertEqual(response.status_code, self.status_ok)

    def test_article_url(self):

        for article in Article.objects.all():
            response = self.client.get(reverse('mainapp:article', kwargs={'pk': article.pk}))
            self.assertEqual(response.status_code, self.status_ok)

    def test_category_url(self):
        for category in Category.objects.all():
            response = self.client.get(reverse('mainapp:category', kwargs={'pk': category.pk}))
            self.assertEqual(response.status_code, self.status_ok)

    def test_comment_create(self):
        response = self.client.get(reverse('mainapp:article', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, self.status_ok)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)

    def test_moderation(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/comment/moderation/')
        self.assertEqual(response.status_code, self.status_ok)

        # open article
        response = self.client.get(reverse('mainapp:aritcle_to_moderate', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, self.status_ok)
        self.assertEqual(self.article.moderated, 0)







