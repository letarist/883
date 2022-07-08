from django.test import TestCase
from mainapp.models import Article
from mainapp.models import Category
from django.test.client import Client

class TestMainappModels(TestCase):
    status_ok = 200
    def setUp(self) -> None:
        self.category = Category.objects.create(
            title='art1'
        )
        for i in range(10):
            Article.objects.create(
                title=f'art-{i}',
                category=self.category,
            )
        self.client = Client()
    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/category/0/1/')
        self.assertEqual(response.status_code, self.status_ok)
