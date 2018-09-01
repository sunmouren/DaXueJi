# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/18 22:43
@desc: users app urls
"""

from django.urls import path, re_path

from .views import LoginView, RegisterView, ActiveUserView, \
    LogoutView, RecommendAuthorListView, UserHomePageView,\
    FollowUserAjax, FollowTopicAjax, UserArticleListView, \
    UserCommentsListView, UserFollowerListView, UserFollowingTopicListView, \
    UserFollowingUserListView, UserActionListView, EditUserProfileView, ForgetPwdView, \
    GetResetPwdView, PostResetPwdView, oauth_weibo, weibo_login

# 要写上app的名字
app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    path('forget/pwd/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('get/reset/(?P<active_code>.*)/', GetResetPwdView.as_view(), name='get_reset_pwd'),
    path('post/reset/pwd/', PostResetPwdView.as_view(), name='post_reset_pwd'),
    path('recommend/', RecommendAuthorListView.as_view(), name='recommend_authors'),
    path('<int:user_id>/homepage/', UserHomePageView.as_view(), name='user_homepage'),
    path('<int:user_id>/articles/', UserArticleListView.as_view(), name='user_articles'),
    path('<int:user_id>/actions/', UserActionListView.as_view(), name='user_actions'),
    path('<int:user_id>/comments/', UserCommentsListView.as_view(), name='user_comments'),
    path('<int:user_id>/followers/', UserFollowerListView.as_view(), name='user_followers'),
    path('<int:user_id>/following/users', UserFollowingUserListView.as_view(), name='user_following_users'),
    path('<int:user_id>/following/topics', UserFollowingTopicListView.as_view(), name='user_following_topics'),
    path('follow/user/', FollowUserAjax.as_view(), name='follow_user'),
    path('follow/topic/', FollowTopicAjax.as_view(), name='follow_topic'),
    path('<int:user_id>/profile/', EditUserProfileView.as_view(), name='edit_profile'),
    # 微博登录授权页面
    path('oauth/weibo/', oauth_weibo, name='oauth_weibo'),
    path('weibo/login/', weibo_login, name='weibo_login'),
]