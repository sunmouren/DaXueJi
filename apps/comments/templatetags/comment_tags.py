# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/24 22:22
@desc: comments app custom template tags
"""

from django import template

from comments.models import Comment

register = template.Library()


@register.simple_tag
def get_comment_list(entry):
    if entry:
        queryset = Comment.objects.filter(article=entry)[:10]
    else:
        queryset = []
    return queryset


@register.simple_tag
def get_most_popular_comments(entry):
    if entry:
        queryset = Comment.objects.filter(article=entry)
        queryset = queryset.exclude(total_like=0).order_by('-total_like')[:10]
    else:
        queryset = []
    return queryset


@register.simple_tag
def check_is_liked_comment(request, users_like):
    """
    检查当前用户是否在评论的喜欢列表中
    """
    is_liked = False
    if request.user.is_authenticated:
        is_liked = request.user in users_like
    return is_liked
