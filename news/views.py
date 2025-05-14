from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import News, Category, Image

# Create your views here.

def home(request):
    """View para a pu00e1gina inicial"""
    # Buscar notu00edcias em destaque
    featured_news = News.objects.filter(is_published=True, featured=True).order_by('-published_at')[:5]
    
    # Buscar notu00edcias recentes
    recent_news = News.objects.filter(is_published=True).order_by('-published_at')[:10]
    
    # Buscar categorias
    categories = Category.objects.all()
    
    return render(request, 'news/home.html', {
        'featured_news': featured_news,
        'recent_news': recent_news,
        'categories': categories
    })

def category_list(request):
    """View para listar todas as categorias"""
    categories = Category.objects.all()
    return render(request, 'news/category_list.html', {
        'categories': categories
    })

def news_list(request):
    """View para listar todas as notícias (com filtros)"""
    # Inicializa o queryset base
    queryset = News.objects.all()
    
    # Filtragem por categoria
    category_slug = request.GET.get('category')
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    
    # Filtragem por publicação
    is_published = request.GET.get('is_published')
    if is_published:
        is_published = is_published.lower() == 'true'
        queryset = queryset.filter(is_published=is_published)
    
    # Filtragem por destaque
    featured = request.GET.get('featured')
    if featured:
        featured = featured.lower() == 'true'
        queryset = queryset.filter(featured=featured)
    
    # Busca
    search_query = request.GET.get('q')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    
    # Ordenação
    ordering = request.GET.get('ordering', '-created_at')
    queryset = queryset.order_by(ordering)
    
    # Paginação
    paginator = Paginator(queryset, 10)  # 10 notícias por página
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    
    # Categorias para o filtro
    categories = Category.objects.all()
    
    return render(request, 'news/news_list.html', {
        'news_list': news,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'ordering': ordering
    })

def news_detail(request, slug):
    """View para exibir detalhes de uma notícia"""
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news/news_detail.html', {
        'news': news
    })

def published_news_list(request):
    """View para listar notícias publicadas"""
    # Inicializa o queryset base
    queryset = News.objects.filter(is_published=True)
    
    # Filtragem por categoria
    category_slug = request.GET.get('category')
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    
    # Filtragem por destaque
    featured = request.GET.get('featured')
    if featured:
        featured = featured.lower() == 'true'
        queryset = queryset.filter(featured=featured)
    
    # Busca
    search_query = request.GET.get('q')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    
    # Ordenação
    ordering = request.GET.get('ordering', '-published_at')
    queryset = queryset.order_by(ordering)
    
    # Paginação
    paginator = Paginator(queryset, 10)  # 10 notícias por página
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    
    # Categorias para o filtro
    categories = Category.objects.all()
    
    return render(request, 'news/published_news_list.html', {
        'news_list': news,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'ordering': ordering
    })

def featured_news_list(request):
    """View para listar notícias em destaque"""
    news_list = News.objects.filter(is_published=True, featured=True).order_by('-published_at')
    return render(request, 'news/featured_news_list.html', {
        'news_list': news_list
    })
