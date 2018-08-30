# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/18 19:35
@desc: 文章模板标签
"""

import mistune

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from ..models import Article


register = template.Library()


@register.simple_tag
def get_recent_article():
    recent_articles = Article.objects.all()[:4]
    return recent_articles


@register.simple_tag
def check_is_liked_article(request, users_like):
    """
    检查当前用户是否在文章的喜欢列表中
    """
    is_liked = False

    if request.user.is_authenticated:
        is_liked = request.user in users_like
    return is_liked


@register.filter(is_safe=True)
@stringfilter
def render_markdown(value):
    return mark_safe(mistune.markdown(value))




