from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    Modelo para categorias de notícias.
    """

    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class News(models.Model):
    """
    Modelo para notícias da paróquia.
    """

    title = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    content = models.TextField("Conteúdo")
    summary = models.TextField("Resumo", max_length=500)

    category = models.ForeignKey(
        Category,
        verbose_name="Categoria",
        on_delete=models.PROTECT,
        related_name="news",
    )

    author = models.ForeignKey(
        User, verbose_name="Autor", on_delete=models.PROTECT, related_name="news"
    )

    cover_image = models.ImageField(
        "Imagem de Capa", upload_to="news/covers/%Y/%m/", blank=True, null=True
    )

    is_published = models.BooleanField(
        "Publicado", default=False, help_text="Indica se a notícia está publicada"
    )

    featured = models.BooleanField(
        "Destaque",
        default=False,
        help_text="Indica se a notícia deve aparecer em destaque",
    )

    created_at = models.DateTimeField("Data de Criação", auto_now_add=True)

    updated_at = models.DateTimeField("Última Atualização", auto_now=True)

    published_at = models.DateTimeField("Data de Publicação", null=True, blank=True)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Image(models.Model):
    """
    Modelo para imagens adicionais das notícias.
    """

    news = models.ForeignKey(
        News, verbose_name="Notícia", on_delete=models.CASCADE, related_name="images"
    )

    image = models.ImageField("Imagem", upload_to="news/images/%Y/%m/")

    caption = models.CharField("Legenda", max_length=200, blank=True)

    order = models.PositiveIntegerField(
        "Ordem", default=0, help_text="Ordem de exibição da imagem"
    )

    created_at = models.DateTimeField("Data de Criação", auto_now_add=True)

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"Imagem {self.order} - {self.news.title}"
