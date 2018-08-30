# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/8/10 13:27
@desc: 一些检查函数
"""
from django.http import Http404


def check_is_request_owner(request, owner):
    """
    检查是当前请求者是为所有者
    :param request:
    :param owner:
    :return: 引发Http404
    """
    if request.user != owner:
        raise Http404
