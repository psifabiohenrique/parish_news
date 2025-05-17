from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "avatar_preview")
    list_filter = ("username", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Informações Pessoais",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "bio",
                    "avatar",
                    "church",
                )
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_pastoral",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "church", "is_staff", "groups"),
            },
        ),
    )
    readonly_fields = ("avatar_preview",)

    def save_model(self, request, obj, form, change):
        if not change:  # Se for um novo usuário
            if not request.user.is_superuser:
                obj.church = request.user.church
            elif not obj.is_superuser and not obj.church:
                # Se for superuser criando um usuário não-superuser, valida a igreja
                raise ValueError("Usuários não-administradores devem estar vinculados a uma igreja")
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        if not obj:  # Caso seja criação de novo usuário
            if request.user.is_superuser:
                return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'password1', 'password2', 'church', 'is_staff', 'groups'),
                    }),
                )
            else:
                return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'password1', 'password2', 'is_staff', 'groups'),
                    }),
                )
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            # Garante que não pode editar esses campos nem via POST
            readonly += [
                "is_superuser",
                "user_permissions",
            ]
        return readonly

    def has_delete_permission(self, request, obj=None):
        # Opcional: só superuser pode deletar usuários
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Opcional: só mostra usuários da mesma igreja
        if request.user.is_superuser:
            return qs
        return qs.filter(church=request.user.church)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.avatar.url,
            )
        return "Sem foto"

    avatar_preview.short_description = "Foto"
