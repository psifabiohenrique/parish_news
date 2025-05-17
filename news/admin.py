from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Category, News, Image
from church.models import Church


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ("image", "caption", "order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" />', obj.image)
        return "Sem imagem"

    image_preview.short_description = "Preview"


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        widgets = {
            "content": forms.Textarea(attrs={"class": "vLargeTextField"}),
            "summary": forms.Textarea(attrs={"rows": 3}),
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(church=request.user.church)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "church" and not request.user.is_superuser:
            kwargs["queryset"] = Church.objects.filter(id=request.user.church.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = (
        "title",
        "author",
        "category",
        "is_published",
        "featured",
        "created_at",
        "image_preview",
    )
    list_filter = ("is_published", "featured", "category", "created_at")
    search_fields = ("title", "content", "summary")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ImageInline]
    date_hierarchy = "created_at"
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="200" />', obj.cover_image)
        return "Sem imagem"

    image_preview.short_description = "Preview"

    def save_model(self, request, obj, form, change):
        if not change:  # Se for uma nova notícia
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(church=request.user.church)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "church" and not request.user.is_superuser:
            kwargs["queryset"] = Church.objects.filter(id=request.user.church.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("news", "order", "caption", "image_preview")
    list_filter = ("news",)
    search_fields = ("news__title", "caption")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" />', obj.image)
        return "Sem imagem"

    image_preview.short_description = "Preview"
