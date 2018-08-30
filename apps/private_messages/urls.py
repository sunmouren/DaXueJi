# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/8/10 12:41
@desc: private messages app url
"""

from django.urls import path

from .views import PrivateMessageListView, PrivateMessageChatView, AddPrivateMessageAJax


app_name = 'private_messages'

urlpatterns = [
    path('list/<int:user_id>/', PrivateMessageListView.as_view(), name='pm_list'),
    path('chat/<int:user_to_id>/', PrivateMessageChatView.as_view(), name='pm_chat'),
    path('add/', AddPrivateMessageAJax.as_view(), name='add_pm'),
]