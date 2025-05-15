from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuário personalizado que estende o modelo padrão do Django.
    """

    is_pastoral = models.BooleanField(
        "Membro da Pastoral",
        default=False,
        help_text="Indica se o usuário é membro da pastoral de comunicação",
    )

    phone = models.CharField("Telefone", max_length=20, blank=True, null=True)

    bio = models.TextField(
        "Biografia", blank=True, help_text="Uma breve descrição sobre o usuário"
    )

    avatar = models.ImageField(
        "Foto de Perfil", upload_to="avatars/", blank=True, null=True
    )

    created_at = models.DateTimeField("Data de Criação", auto_now_add=True)

    updated_at = models.DateTimeField("Última Atualização", auto_now=True)

    church = models.ForeignKey(
        "church.Church",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
        help_text="Igreja à qual o usuário está vinculado. Obrigatório para usuários não-administradores."
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-date_joined"]

    def save(self, *args, **kwargs):
        if not self.is_superuser and not self.church:
            raise ValueError("Usuários não-administradores devem estar vinculados a uma igreja")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() or self.username