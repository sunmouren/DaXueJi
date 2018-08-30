# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/19 16:48
@desc: users app custom template tags
"""

from django import template

from ..models import UserProfile, FollowTopic, FollowUser

register = template.Library()


@register.simple_tag
def get_recommend_authors(request, num=3):
    """
    获取推荐用户，其中不包括已关注的粉丝和自己
    :param request:
    :param num: 推荐用户切片数量
    :return:
    """
    recommend_authors = UserProfile.objects.exclude(id=request.user.id)
    # if request.user.is_authenticated:
    #     following_ids = request.user.following_user.values_list('id', flat=True)
    #     if following_ids:
    #         suggested_users = recommend_authors.exclude(id__in=following_ids)
    return recommend_authors[:num]


@register.simple_tag
def check_is_following_topic(request, topic):
    is_following = False
    if request.user.is_authenticated and topic:
        following_topics = FollowTopic.objects.filter(user=request.user, topic=topic)
        if following_topics:
            is_following = True
    return is_following


@register.simple_tag
def check_is_following_user(request, user):
    is_following = False
    if request.user.is_authenticated and user:
        following_topics = FollowUser.objects.filter(user_from=request.user, user_to=user)
        if following_topics:
            is_following = True
    return is_following



