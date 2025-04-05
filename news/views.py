from django.shortcuts import render
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import News, Category
from .serializers import (
    NewsSerializer,
    NewsCreateSerializer,
    NewsUpdateSerializer,
    CategorySerializer
)

# Create your views here.

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class NewsListView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_published', 'featured']
    search_fields = ['title', 'content', 'summary']
    ordering_fields = ['created_at', 'updated_at', 'published_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewsCreateSerializer
        return NewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return NewsUpdateSerializer
        return NewsSerializer

class PublishedNewsListView(generics.ListAPIView):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'content', 'summary']
    ordering_fields = ['published_at', 'created_at']

class FeaturedNewsListView(generics.ListAPIView):
    queryset = News.objects.filter(is_published=True, featured=True)
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['published_at']
