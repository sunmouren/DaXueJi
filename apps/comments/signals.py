# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/27 14:16
@desc: data change signals，记得在__init__.py和apps中做相应的配置
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Comment


@receiver(m2m_changed, sender=Comment.user_like.through)
def user_like_changed(sender, instance, **kwargs):
    instance.total_like = instance.user_like.count()
    instance.save()