# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/18 20:12
@desc: writing app urls
"""

from django.urls import path, re_path

from .views import ArticleDetailView, LikeArticleAjax, \
    AddArticleView, EditArticleView, DeleteArticleAjax, ArticleListView

# 要写上app的名字
app_name = "writing"

urlpatterns = [
    path('list/', ArticleListView.as_view(), name='article_list'),
    path('detail/<int:article_id>/', ArticleDetailView.as_view(), name="article_detail"),
    path('like/', LikeArticleAjax.as_view(), name='like_article'),
    path('add/', AddArticleView.as_view(), name='add_article'),
    path('edit/<int:article_id>/', EditArticleView.as_view(), name="edit_article"),
    path('delete/', DeleteArticleAjax.as_view(), name="delete_article"),
]