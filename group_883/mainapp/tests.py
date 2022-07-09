from django.test import TestCase
from mainapp.models import Article
from mainapp.models import Category
from django.test.client import Client
from personal_account.models import User


class TestMainappModels(TestCase):
    status_ok = 200
    status_redirect = 302

    def setUp(self) -> None:
        self.category = Category.objects.create(
            title='art1'
        )
        self.user = User.objects.create(
            description='desc1'
        )
        for i in range(10):
            Article.objects.create(
                title=f'art-{i}',
                category=self.category,
                user=self.user
            )
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/category/0/1/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/category/7/1/')
        self.assertEqual(response.status_code, self.status_ok)

    def test_mainapp_articles(self):
        for article in Article.objects.all():
            response = self.client.get(f'/article/<int:pk>/{article}')
            self.assertEqual(response.status_code, self.status_ok)

    def test_comments(self):
        pass


