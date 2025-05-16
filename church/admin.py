# churches/admin.py
from django.contrib import admin
from .models import Church, Priest


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name", "website")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(id=request.user.church.id)


@admin.register(Priest)
class PriestAdmin(admin.ModelAdmin):
    list_display = ("name", "church", "title", "active")
    list_filter = ("church", "active")
    search_fields = ("name", "church__name")
    fieldsets = (
        # (None, {"fields": {"name"}}),
        ("Informações do padre",
        {
            "fields": (
                "name",
                "slug",
                "title",
                "function",
                "history",
                "message",
                "photo",
                "active",
            )
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(church=request.user.church)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.church = request.user.church
        super().save_model(request, obj, form, change)
