# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/8/10 15:00
@desc: private messages template tags
"""

from django import template


register = template.Library()


@register.simple_tag
def get_leaf_node(node):
    """
    获取叶子节点
    :param node:
    :return:
    """
    descendants = list(node.get_descendants(include_self=True))
    return descendants[-1] if descendants else None

