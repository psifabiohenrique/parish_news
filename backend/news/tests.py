from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, News
from django.contrib.auth.models import User

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_category_creation(self):
        """Test if a category can be created"""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_slug_auto_generation(self):
        """Test if slug is automatically generated from name"""
        category = Category.objects.create(name='Another Category')
        self.assertEqual(category.slug, 'another-category')

    def test_category_unique_slug(self):
        """Test if duplicate slugs are handled correctly"""
        # Try to create a category with the same name
        category2 = Category.objects.create(name='Test Category')
        self.assertNotEqual(category2.slug, 'test-category')
        self.assertTrue(category2.slug.startswith('test-category-'))

class NewsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.news = News.objects.create(
            title='Test News',
            slug='test-news',
            content='Test content',
            category=self.category,
            is_published=True,
            is_featured=True
        )

    def test_news_creation(self):
        """Test if a news article can be created"""
        self.assertEqual(self.news.title, 'Test News')
        self.assertEqual(self.news.slug, 'test-news')
        self.assertEqual(self.news.content, 'Test content')
        self.assertEqual(self.news.category, self.category)
        self.assertTrue(self.news.is_published)
        self.assertTrue(self.news.is_featured)
        self.assertTrue(isinstance(self.news, News))
        self.assertEqual(str(self.news), 'Test News')

    def test_news_slug_auto_generation(self):
        """Test if slug is automatically generated from title"""
        news = News.objects.create(
            title='Another News',
            content='Test content',
            category=self.category
        )
        self.assertEqual(news.slug, 'another-news')

    def test_news_unique_slug(self):
        """Test if duplicate slugs are handled correctly"""
        news2 = News.objects.create(
            title='Test News',
            content='Test content',
            category=self.category
        )
        self.assertNotEqual(news2.slug, 'test-news')
        self.assertTrue(news2.slug.startswith('test-news-'))

    def test_news_default_values(self):
        """Test default values for news article"""
        news = News.objects.create(
            title='Default News',
            content='Test content',
            category=self.category
        )
        self.assertFalse(news.is_published)
        self.assertFalse(news.is_featured)
        self.assertIsNotNone(news.created_at)
        self.assertIsNotNone(news.updated_at)

class NewsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.news = News.objects.create(
            title='Test News',
            slug='test-news',
            content='Test content',
            category=self.category,
            is_published=True,
            is_featured=True
        )
        self.unpublished_news = News.objects.create(
            title='Unpublished News',
            slug='unpublished-news',
            content='Unpublished content',
            category=self.category,
            is_published=False
        )

    def test_get_news_list(self):
        """Test retrieving list of published news"""
        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only published news
        self.assertEqual(response.data[0]['title'], 'Test News')

    def test_get_news_detail(self):
        """Test retrieving a single news article"""
        url = reverse('news-detail', kwargs={'slug': self.news.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test News')
        self.assertEqual(response.data['content'], 'Test content')

    def test_get_unpublished_news(self):
        """Test that unpublished news is not accessible"""
        url = reverse('news-detail', kwargs={'slug': self.unpublished_news.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_featured_news(self):
        """Test retrieving featured news"""
        url = reverse('news-list')
        response = self.client.get(url, {'featured': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test News')

    def test_get_news_by_category(self):
        """Test filtering news by category"""
        url = reverse('news-list')
        response = self.client.get(url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test News')

    def test_category_list(self):
        response = self.client.get('/api/categories/')  # Substitua pela sua URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Verifica se há categorias

    def test_news_list(self):
        response = self.client.get('/api/news/')  # Substitua pela sua URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Verifica se há notícias

    def test_create_news_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/api/news/', {
            'title': 'New Test News',
            'content': 'Content for new test news.',
            'summary': 'New summary',
            'category': self.category.id,
            'is_published': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_published_news_list(self):
        response = self.client.get('/api/news/published/')  # Substitua pela sua URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Verifica se há notícias publicadas

    def test_featured_news_list(self):
        response = self.client.get('/api/news/featured/')  # Substitua pela sua URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Verifica se há notícias em destaque

class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_get_category_list(self):
        """Test retrieving list of categories"""
        url = reverse('categories/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Category')

