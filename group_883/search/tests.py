from django.test import TestCase
from django.test.client import Client
from mainapp.models import Category, Article, Tag, Comment
from personal_account.models import User
from django.urls import reverse
from search.filters import ArticleFilter
class TestMainappSmoke(TestCase):
    status_ok = 200
    status_redirect = 302
    def setUp(self) -> None:


        self.category = Category.objects.create(
            title='Все потоки'
        )

        self.tag = Tag.objects.create(
            title='Java'
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
        self.client = Client()

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
                body='body')

    def test_search_urls(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/24')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/14')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/15')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/?q=')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/#')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/popular/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/popular/#')
        self.assertEqual(response.status_code, self.status_ok)

    def test_input_user(self):
        response = self.client.get('/search/?category=&user=&created_at__lt=&created_at__gt=&tag=14')
        self.assertEqual(response.status_code, self.status_ok)
        response = self.client.get('?category=&user=7&created_at__lt=&created_at__gt=')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('?category=&user=9&created_at__lt=&created_at__gt=&tag=13')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('?category=&user=14&created_at__lt=&created_at__gt=')
        self.assertEqual(response.status_code, self.status_ok)

    def test_article_page(self):
        response = self.client.get('/search/?q=&page=1')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/?q=&page=2')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/?q=&page=3')
        self.assertEqual(response.status_code, self.status_ok)

    def test_search_popular(self):
        response = self.client.get('/search/24')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/14')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/search/13')
        self.assertEqual(response.status_code, self.status_ok)



# Create your tests here.
