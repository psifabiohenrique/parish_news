from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('categories/', views.category_list, name='category_list'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('priest/', views.priest, name='priest'),
    path('about/', views.about, name='about'),
    path('test-colors/', views.test_colors, name='test_colors'),  # Página de teste das cores
] 