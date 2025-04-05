from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Modelo de usuário personalizado que estende o modelo padrão do Django.
    """
    is_pastoral = models.BooleanField(
        'Membro da Pastoral',
        default=False,
        help_text='Indica se o usuário é membro da pastoral de comunicação'
    )
    
    phone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        null=True
    )
    
    bio = models.TextField(
        'Biografia',
        blank=True,
        help_text='Uma breve descrição sobre o usuário'
    )
    
    avatar = models.ImageField(
        'Foto de Perfil',
        upload_to='avatars/',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(
        'Data de Criação',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'Última Atualização',
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
        permissions = [
            ("can_manage_news", "Pode gerenciar notícias"),
            ("can_publish_news", "Pode publicar notícias"),
            ("can_manage_categories", "Pode gerenciar categorias"),
            ("can_manage_images", "Pode gerenciar imagens"),
        ]
    
    def __str__(self):
        return self.get_full_name() or self.username
