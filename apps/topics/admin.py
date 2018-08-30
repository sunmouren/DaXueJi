from django.contrib import admin

from .models import Topic, RecordArticle


class TopicAdmin(admin.ModelAdmin):
    """
    专题管理
    """
    list_display = ['name', 'summary', 'created']
    search_fields = ['name', 'summary']
    list_filter = ['name', 'created']


class RecordArticleAdmin(admin.ModelAdmin):
    """
    收录文章管理
    """
    list_display = ['topic', 'article', 'is_pass', 'created']
    search_fields = ['topic', 'article']
    list_filter = ['topic', 'is_pass']


admin.site.register(Topic, TopicAdmin)
admin.site.register(RecordArticle, RecordArticleAdmin)
