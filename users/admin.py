from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User
from .forms import CustomUserCreationForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'avatar_preview')
    list_filter = ('username', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'phone', 'bio', 'avatar', 'church')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_pastoral', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'groups'),
        }),
    )
    readonly_fields = ('avatar_preview',)

    # add_form = CustomUserCreationForm

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Use special form during user creation
    #     """
    #     defaults = {}
    #     if obj is None:
    #         defaults['form'] = self.add_form
    #     defaults.update(kwargs)
    #     form = super().get_form(request, obj, **defaults)
    #     if obj is None and not request.user.is_superuser:
    #         # Se estiver criando um novo usuário e não for superuser
    #         form.base_fields['church'].queryset = User.objects.filter(
    #             id=request.user.church.id
    #         ).values_list('church', flat=True)
    #     return form

    def save_model(self, request, obj, form, change):
        if not change:
            # Se for um novo usuário, atribua a igreja do usuário logado
            if not request.user.is_superuser:
                obj.church = request.user.church
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Se não for superuser, remove os campos sensíveis
        if not request.user.is_superuser:
            new_fieldsets = []
            for name, opts in fieldsets:
                fields = list(opts.get('fields', []))
                # Remove campos sensíveis
                for sensitive in ['is_superuser', 'user_permissions', 'church']:
                    if sensitive in fields:
                        fields.remove(sensitive)
                new_fieldsets.append((name, {'fields': fields}))
            return new_fieldsets
        return fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            # Garante que não pode editar esses campos nem via POST
            readonly += ['is_superuser', 'user_permissions',]
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
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "Sem foto"
    avatar_preview.short_description = 'Foto'
