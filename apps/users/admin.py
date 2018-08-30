from django.contrib import admin

from .models import UserProfile, EmailVerifyRecord, FollowUser, FollowTopic


class UserProfileAdmin(admin.ModelAdmin):
    """
    用户信息管理
    """
    list_display = ['username', 'nickname', 'signature', 'gender', 'date_joined', 'avatar']
    search_fields = ['username', 'nickname', 'signature', 'gender']
    list_filter = ['gender', 'date_joined']


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    """
    邮箱验证管理
    """
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class FollowUserAdmin(admin.ModelAdmin):
    """
    关注用户管理
    """
    list_display = ['user_from', 'user_to', 'created']
    search_fields = ['user_from', 'user_to']
    list_filter = ['created']


class FollowTopicAdmin(admin.ModelAdmin):
    """
    关注话题管理
    """
    list_display = ['user', 'topic', 'created']
    search_fields = ['user', 'topic']
    list_filter = ['created']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
admin.site.register(FollowUser, FollowUserAdmin)
admin.site.register(FollowTopic, FollowTopicAdmin)
