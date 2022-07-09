from django.test import TestCase
from django.test.client import Client
from mainapp.models import Category, Article, Tag, Comment
from personal_account.models import User


class TestMainappSmoke(TestCase):
    status_ok = 200

    def setUp(self) -> None:
        self.category = Category.objects.create(
            title='Разработка'
        )
        self.tag = Tag.objects.create(
            title='Python'
        )
        self.user = User.objects.create(
            description='description',
            username='username',
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
        for i in range(10):
            Article.objects.create(
                category=self.category,
                user=self.user,
                tag=self.tag,
                title=f'title {i}',
                short_desc=f'short description {i}',
                body=f'body {i}',
            )
        self.comment = Comment.objects.create(
            article=self.article,
            user=self.user,
            body='body'
        )
        self.client = Client()

    def test_mainapp_url(self):
        """test if main page and page help are opened"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/help/')
        self.assertEqual(response.status_code, self.status_ok)

    # def test_article_url(self):
    #     pass
    #
    # def tearDown(self) -> None:
    #     pass
