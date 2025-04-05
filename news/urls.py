from django.urls import path
from .views import (
    CategoryListView,
    NewsListView,
    NewsDetailView,
    PublishedNewsListView,
    FeaturedNewsListView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('published/', PublishedNewsListView.as_view(), name='published_news_list'),
    path('featured/', FeaturedNewsListView.as_view(), name='featured_news_list'),
] 