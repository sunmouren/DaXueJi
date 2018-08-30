# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/24 23:12
@desc: comments app urls
"""

from django.urls import path

from .views import SubmitCommentAjax, LikeCommentAjax, DeleteCommentAJax

app_name = "comments"


urlpatterns = [
    path('submit/', SubmitCommentAjax.as_view(), name='submit_comment'),
    path('like/', LikeCommentAjax.as_view(), name='like_comment'),
    path('delete/', DeleteCommentAJax.as_view(), name='delete_comment'),
]