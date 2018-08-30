# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/8/13 16:18
@desc: 因为我们在视图层都是继承View，所以不能直接用装饰器（类似@login_required),
        所以也要用继承的方式
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/user/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)