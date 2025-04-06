from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Category, News
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
import io
import tempfile
from django.test import override_settings
import shutil


TEMP_MEDIA_ROOT = tempfile.mkdtemp()

class CategoryListViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

    def test_get_categories(self):
        response = self.client.get(
            reverse("category_list")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.category.name)

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class NewsListViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        self.news = News.objects.create(
            title="Test News",
            content="Content for test news.",
            summary="Test summary",
            category=self.category,
            author=self.user,
            cover_image="test.jpg",
        )

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_get_news_list(self):
        response = self.client.get(
            reverse("news_list")
        )  # Adjust the URL name as necessary
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.news.title)

    def test_create_news(self):
        image = PILImage.new("RGB", (100, 100), color="red")
        tmp_file = io.BytesIO()
        image.save(tmp_file, format="JPEG")
        tmp_file.seek(0)

        test_image = SimpleUploadedFile(
            name="test.jpg", content=tmp_file.read(), content_type="image/jpeg"
        )
        data = {
            "title": "New Test News",
            "content": "Content for new test news.",
            "summary": "New test summary",
            "category": self.category.id,
            "cover_image": test_image,
        }
        response = self.client.post(reverse("news_list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            News.objects.count(), 2
        )  # Check if a new news item was created


class NewsDetailViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")
        self.news = News.objects.create(
            title="Test News",
            content="Content for test news.",
            summary="Test summary",
            category=self.category,
            author=self.user,
            cover_image="test.jpg",
        )

    def test_get_news_detail(self):
        response = self.client.get(
            reverse("news_detail", kwargs={"slug": self.news.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.news.title)

    def test_update_news(self):
        data = {
            "title": "Updated Test News",
            "content": "Updated content for test news.",
            "summary": "Updated test summary",
            "category": self.category.id,
        }
        response = self.client.put(
            reverse("news_detail", kwargs={"slug": self.news.slug}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, "Updated Test News")

    def test_delete_news(self):
        response = self.client.delete(
            reverse("news_detail", kwargs={"slug": self.news.slug}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.count(), 0)  # Check if the news item was deleted


class PublishedNewsListViewTest(APITestCase):
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
            is_published=True,
        )

    def test_get_published_news(self):
        response = self.client.get(
            reverse("published_news_list")
        )  # Adjust the URL name as necessary
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.news.title)


class FeaturedNewsListViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.news = News.objects.create(
            title="Featured News",
            content="Content for featured news.",
            summary="Featured summary",
            category=self.category,
            author=self.user,
            cover_image="test.jpg",
            is_published=True,
            featured=True,
        )

    def test_get_featured_news(self):
        response = self.client.get(
            reverse("featured_news_list")
        )  # Adjust the URL name as necessary
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.news.title)
