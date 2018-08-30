# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/8/4 20:55
@desc: the action utils
"""

import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(user, verb, target=None):
    """
    Generate the action
    :param user: action from user
    :param verb: user verb describe
    :param target: action from instance
    :return: boolean
    """
    # 防止记录一分钟重复的动作
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True

    return False


def check_is_empty_and_delete(action=None):
    """
    检查活动是否为空，并删除
    :param target:
    :return:
    """
    pass
