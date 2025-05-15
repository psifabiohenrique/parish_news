# churches/admin.py
from django.contrib import admin
from .models import Church, Priest

@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name', 'website')

@admin.register(Priest)
class PriestAdmin(admin.ModelAdmin):
    list_display = ('name', 'church', 'title', 'active')
    list_filter = ('church', 'active')
    search_fields = ('name', 'church__name')
