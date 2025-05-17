from django.db import models
from django.core.validators import URLValidator
from django.utils.text import slugify


class Church(models.Model):
    """Modelo para representar uma igreja"""

    name = models.CharField("Nome", max_length=255)
    slug = models.SlugField("Slug", unique=True, max_length=255)
    phone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("Email", max_length=255, blank=True, null=True)
    opening_hours = models.TextField("Horário de Funcionamento", blank=True, null=True)
    history = models.TextField("História", blank=True, null=True)
    patron = models.TextField("Padroeiro", blank=True, null=True)
    mass_schedule = models.TextField("Horário das Missas", blank=True, null=True)
    location_contact = models.TextField("Contato e Localização", blank=True, null=True)
    pastorals_movement = models.TextField(
        "Pastorais e Movimentos", blank=True, null=True
    )
    confessions = models.TextField("Confissões e atendimentos", blank=True, null=True)

    website = models.URLField("Website", blank=True, null=True)

    class Meta:
        verbose_name = "Igreja"
        verbose_name_plural = "Igrejas"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Priest(models.Model):
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="priests")
    name = models.CharField("Nome", max_length=255)
    slug = models.SlugField("Slug", unique=True, max_length=255)
    title = models.CharField(
        "Título (padre, bispo, etc.)", max_length=255, blank=True, null=True
    )
    function = models.CharField(
        "Função (pároco, vigário, etc.)", max_length=255, blank=True, null=True
    )
    history = models.TextField("Formação e Trajetória", blank=True, null=True)
    message = models.TextField("Mensagem para a comunidade", blank=True, null=True)
    photo = models.URLField(
        "Foto do padre",
        max_length=1000,
        validators=[URLValidator()],
        blank=True,
        null=True,
    )
    active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Padre"
        verbose_name_plural = "Padres"

    def __str__(self):
        return f"{self.title} {self.name} - {self.church.name}"
