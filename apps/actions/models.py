from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from topics.models import Topic
from writing.models import Article


class Action(models.Model):
    """
    用户活动表
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='actions', db_index=True)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                  blank=True, null=True,
                                  related_name='target_obj')
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = '用户活动'
        verbose_name_plural = verbose_name
        ordering = ('-created',)










