from django.db import models
from django.conf import settings

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from writing.models import Article


class Comment(MPTTModel):
    """
    多级评论表
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='user_comments', verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='comments', verbose_name='文章')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='父级评论')
    content = models.TextField(verbose_name='评论内容', default='')
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='liked_comments',
                                       blank=True)
    total_like = models.PositiveIntegerField(verbose_name='喜欢数', default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class MPPTTMeta:
        order_insertion_by = ['-created']

    def __str__(self):
        if self.parent is not None:
            return '{0} 回复 {1}'.format(self.user.username, self.parent.user.username)
        else:
            return '{0} 评论了 {1}'.format(self.user.username, self.article)
