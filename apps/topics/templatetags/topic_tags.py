# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/19 23:51
@desc: topics app custom template tags
"""

from django import template

from ..models import Topic


register = template.Library()


@register.simple_tag
def get_hot_topics(num=6):
    hot_topics = Topic.objects.all()[:num]
    return hot_topics


