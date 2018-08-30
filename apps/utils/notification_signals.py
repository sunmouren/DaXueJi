# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/8/5 22:48
@desc: 通知
"""

from django.db.models.signals import post_save

from notifications.signals import notify

from comments.models import Comment
from users.models import UserProfile


def comment_handler(sender, instance, created, **kwargs):
    """
    评论通知
    :param sender: 发送者
    :param instance: 评论实例
    :param created: 时间
    :param kwargs:
    :return:
    """
    # 避免自己接收自己评论通知
    recipients = UserProfile.objects.exclude(id=instance.user.id)
    # 判断是评论还是回复
    if instance.parent is not None:
        recipient = instance.parent.user
        verb = '回复了你'
    else:
        recipient = instance.article.author
        verb = '评论了你'

    # 发送通知
    if recipient in recipients:
        notify.send(instance.user, recipient=recipient,
                    verb=verb, action_object=instance,
                    target=instance.article, description=instance.content)

post_save.connect(comment_handler, sender=Comment)