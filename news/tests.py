from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from news.models import Article
import logging


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student_07",
            password="password123",
            email="test@test.com"
        )
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            author=self.user
        )
    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.content, "This is a test article.")
        self.assertEqual(self.article.author.username, "student_07")

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test Article")


class ArticleAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student_07",
            email="student_07@step.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe"
        )
        Article.objects.create(
            title='Test Article 1',
            content='This is the content of test article 1.',
            author=self.user
        )
        self.url = '/api/v1/news/'

    def test_get_news(self):
        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(data) > 0)

        # print('-- Results --')
        # print('-- Status --', self.assertEqual)
        # print('-- Have news --', self.assertTrue)
        # print('-- Data QTY --', len(data))


    def test_create_article(self):
        data = {
            'title': 'New Test Article',
            'content': 'This is the content of the new test article.',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_get_news()


