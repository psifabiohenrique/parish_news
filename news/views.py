from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import News, Category
from church.models import Church, Priest

# Create your views here.


def home(request, church_slug):
    church = get_object_or_404(Church, slug=church_slug)
    
    # Buscar noticias em destaque
    featured_news = News.objects.filter(is_published=True, featured=True, church__slug=church_slug).order_by(
        "-published_at"
    )[:5]

    # Buscar notícias recentes
    recent_news = News.objects.filter(is_published=True, church__slug=church_slug).order_by("-published_at")[:10]

    # Buscar categorias
    categories = Category.objects.filter(church__slug=church_slug)

    return render(
        request,
        "news/home.html",
        {
            "featured_news": featured_news,
            "recent_news": recent_news,
            "categories": categories,
            "church": church,
            "church_slug": church_slug,
        },
    )


def category_list(request, church_slug):
    """View para listar todas as categorias"""
    church = get_object_or_404(Church, slug=church_slug)
    categories = Category.objects.filter(church__slug=church_slug)
    return render(request, "news/category_list.html", {
        "categories": categories,
        "church": church,
        "church_slug": church_slug
    })


def news_list(request, church_slug):
    """View para listar todas as notícias (com filtros)"""
    church = get_object_or_404(Church, slug=church_slug)
    
    # Inicializa o queryset base
    queryset = News.objects.filter(is_published=True, church__slug=church_slug)

    # Filtragem por categoria
    category_slug = request.GET.get("category")
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    # Filtragem por destaque
    featured = request.GET.get("featured")
    if featured:
        featured = featured.lower() == "true"
        queryset = queryset.filter(featured=featured)

    # Busca
    search_query = request.GET.get("q")
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(summary__icontains=search_query)
        )

    # Ordenação
    ordering = request.GET.get("ordering", "-published_at")
    queryset = queryset.order_by(ordering)

    # Paginação
    paginator = Paginator(queryset, 10)  # 10 notícias por página
    page = request.GET.get("page")
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    # Categorias para o filtro
    categories = Category.objects.filter(church__slug=church_slug)

    return render(
        request,
        "news/news_list.html",
        {
            "news_list": news,
            "categories": categories,
            "current_category": category_slug,
            "search_query": search_query,
            "ordering": ordering,
            "church": church,
            "church_slug": church_slug,
        },
    )


def news_detail(request, church_slug, slug):
    """View para exibir detalhes de uma notícia"""
    news = get_object_or_404(News, slug=slug)
    church = get_object_or_404(Church, slug=church_slug)
    return render(request, "news/news_detail.html", {"news": news, "church": church})


def published_news_list(request, church_slug):
    """View para listar notícias publicadas"""
    # Inicializa o queryset base
    queryset = News.objects.filter(is_published=True, church__slug=church_slug)

    # Filtragem por categoria
    category_slug = request.GET.get("category")
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    # Filtragem por destaque
    featured = request.GET.get("featured")
    if featured:
        featured = featured.lower() == "true"
        queryset = queryset.filter(featured=featured)

    # Busca
    search_query = request.GET.get("q")
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(summary__icontains=search_query)
        )

    # Ordenação
    ordering = request.GET.get("ordering", "-published_at")
    queryset = queryset.order_by(ordering)

    # Paginação
    paginator = Paginator(queryset, 10)  # 10 notícias por página
    page = request.GET.get("page")
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    # Categorias para o filtro
    categories = Category.objects.filter(church__slug=church_slug)

    return render(
        request,
        "news/published_news_list.html",
        {
            "news_list": news,
            "categories": categories,
            "current_category": category_slug,
            "search_query": search_query,
            "ordering": ordering,
        },
    )


def about(request, church_slug):
    """View para a página sobre a paróquia"""
    church = get_object_or_404(Church, slug=church_slug)
    return render(request, "news/about.html", {"church": church, "church_slug": church_slug})


def priest(request, church_slug):
    """View para a página do pároco"""
    church = get_object_or_404(Church, slug=church_slug)
    queryset = Priest.objects.filter(church__slug=church_slug)
    return render(request, "news/priest.html", {"priests": queryset, "church": church, "church_slug": church_slug})
