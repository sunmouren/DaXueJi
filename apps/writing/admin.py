from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'view_count']
    list_filter = ['created']


admin.site.register(Article, ArticleAdmin)