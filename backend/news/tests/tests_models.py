from django.test import TestCase
from django.utils import timezone

from ..models import Category, News, Image
from users.models import User


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.slug, "test-category")
        self.assertEqual(self.category.description, "")

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_category_description(self):
        self.category.description = "This is a test description."
        self.category.save()
        self.assertEqual(self.category.description, "This is a test description.")


class NewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.news = News.objects.create(
            title="Test News",
            content="Content for test news.",
            summary="Test summary",
            category=self.category,
            author=self.user,
            cover_image="test.jpg",
        )

    def test_news_creation(self):
        self.assertEqual(self.news.title, "Test News")
        self.assertEqual(self.news.content, "Content for test news.")
        self.assertEqual(self.news.summary, "Test summary")
        self.assertEqual(self.news.category, self.category)
        self.assertEqual(self.news.author, self.user)
        self.assertEqual(self.news.slug, "test-news")
        self.assertEqual(self.news.cover_image, "test.jpg")

    def test_news_str_representation(self):
        self.assertEqual(str(self.news), "Test News")

    def test_news_default_fields(self):
        self.assertFalse(self.news.is_published)
        self.assertFalse(self.news.featured)

    def test_news_published_at(self):
        self.news.published_at = timezone.now()
        self.news.save()
        self.assertIsNotNone(self.news.published_at)

    def test_news_slug_generation(self):
        news2 = News.objects.create(
            title="Test News",
            content="Another content for test news.",
            summary="Another test summary",
            category=self.category,
            author=self.user,
            cover_image="test2.jpg",
        )
        self.assertEqual(news2.slug, "test-news-1")  # Assuming slug generation works correctly


class ImageTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.news = News.objects.create(
            title="Test News",
            content="Content for test news.",
            summary="Test summary",
            category=self.category,
            author=self.user,
            cover_image="test.jpg",
        )
        self.image = Image.objects.create(
            news=self.news,
            image="test.jpg",
            caption="Test caption",
        )

    def test_image_creation(self):
        self.assertEqual(self.image.news, self.news)
        self.assertEqual(self.image.image, "test.jpg")
        self.assertEqual(self.image.caption, "Test caption")

    def test_image_str_representation(self):
        self.assertEqual(
            str(self.image), f"Imagem {self.image.order} - {self.news.title}"
        )

    def test_image_order(self):
        self.image.order = 1
        self.image.save()
        self.assertEqual(self.image.order, 1)
