# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/19 22:42
@desc: topics app urls
"""

from django.urls import path, re_path

from .views import HotTopicListView, TopicDetailView, \
    RecordArticleAjax, CanRecordArticleAJax, TopicArticleListView, \
    TopicArticleCommentListView, TopicFollowerListView

app_name = 'topics'

urlpatterns = [
    path('hot/', HotTopicListView.as_view(), name='hot_topics'),
    path('detail/<int:topic_id>/', TopicDetailView.as_view(), name='topic_detail'),
    path('<int:topic_id>/articles/', TopicArticleListView.as_view(), name='topic_articles'),
    path('<int:topic_id>/comments/', TopicArticleCommentListView.as_view(), name='topic_comments'),
    path('<int:topic_id>/followers/', TopicFollowerListView.as_view(), name='topic_followers'),
    path('record/article', RecordArticleAjax.as_view(), name='record_article'),
    path('can/record/article', CanRecordArticleAJax.as_view(), name="can_record_article"),

]