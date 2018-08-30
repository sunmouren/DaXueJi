from django.db import models
from django.conf import settings
from django.urls import reverse

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class PrivateMessage(MPTTModel):
    """
    私信表
    """
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='sent_messages', verbose_name='发送者')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='received_messages', verbose_name='接收者')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='父级私信')
    content = models.TextField(verbose_name='私信内容')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        if self.parent is not None:
            return '{0} 回复了 {1} 私信'.format(self.user_from, self.user_to)
        else:
            return '{0} 私信了 {1}'.format(self.user_from, self.user_to)
