from django.db import models
import uuid
import os
from django.core.exceptions import ValidationError
from django.utils.text import slugify


# Create your models here.
def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"

    if isinstance(instance, Priest):
        return os.path.join("priest/image", filename)
    return os.path.join("priest/images", filename)


def validate_image_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not ext.lower() in valid_extensions:  # noqa: E713
        raise ValidationError(
            "Formato de arquivo não suportado. Use JPG, JPEG, PNG ou GIF."
        )


class Church(models.Model):
    """Modelo para representar uma igreja"""

    name = models.CharField("Nome", max_length=255)
    slug = models.SlugField("Slug", unique=True, max_length=255)
    history = models.TextField("História", blank=True, null=True)
    patron = models.TextField("Padroeiro", blank=True, null=True)
    mass_schedule = models.TextField("Horário das Missas", blank=True, null=True)
    location_contact = models.TextField("Contato e Localização", blank=True, null=True)
    pastorals_movement = models.TextField(
        "Pastorais e Movimentos", blank=True, null=True
    )

    website = models.URLField("Website", blank=True, null=True)

    class Meta:
        verbose_name = 'Church'
        verbose_name_plural = 'Churches'
    
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
    title = models.CharField("Título", max_length=255, blank=True, null=True)
    photo = models.ImageField(
        "Foto",
        upload_to=get_file_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
    )
    active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"{self.title} {self.name} - {self.church.name}"
        