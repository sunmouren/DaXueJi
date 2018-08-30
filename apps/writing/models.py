from django.db import models
from django.urls import reverse
from django.conf import settings


class Article(models.Model):
    """
    文章表
    """
    title = models.CharField(verbose_name='标题', blank=True, null=True, max_length=128, default='随笔')
    summary = models.CharField(verbose_name='摘要', blank=True, null=True, max_length=128)
    content = models.TextField(verbose_name='文章内容')
    cover_picture = models.ImageField(upload_to='image/article', blank=True, null=True, verbose_name='封面图片')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='articles', verbose_name='作者')
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='liked_articles',
                                       blank=True)
    total_like = models.PositiveIntegerField(verbose_name='喜欢数', default=0, db_index=True)
    view_count = models.PositiveIntegerField(verbose_name='阅读数', default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    # 获取文章绝对路径
    def get_absolute_url(self):
        return reverse('writing:article_detail', args=[self.id])

    # 当文章被点击时，阅读数+1
    def view_count_increase(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def __str__(self):
        return self.title
