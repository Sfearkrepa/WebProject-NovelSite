from django.contrib import admin
from .models import Novel


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'chapters_count')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'author', 'description')
    ordering = ('-published_date',)