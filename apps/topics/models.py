from django.db import models
from django.urls import reverse
from django.conf import settings

from writing.models import Article


class Topic(models.Model):
    """
    专题表
    """
    name = models.CharField(verbose_name='专题名', max_length=64)
    summary = models.CharField(verbose_name='简介', blank=True, null=True, max_length=128)
    avatar = models.ImageField(upload_to='image/%Y%m',
                               default='image/default.jpg')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              blank=True, null=True, related_name='admin_topics')
    articles = models.ManyToManyField(Article, through='RecordArticle', symmetrical=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '专题'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    # 获取专题绝对路径
    def get_absolute_url(self):
        return reverse('topics:topic_detail', args=[self.id])

    # 获取专题收录的文章全部列表
    def get_article_list(self):
        return reverse('topics:topic_articles', args=[self.id])

    # 获取专题收录的文章评论列表
    def get_article_comment_list(self):
        return reverse('topics:topic_comments', args=[self.id])

    # 获取专题粉丝列表
    def get_follower_list(self):
        return reverse('topics:topic_followers', args=[self.id])

    def __str__(self):
        return self.name


class RecordArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='投稿文章')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='投稿专题')
    is_pass = models.BooleanField(default=False, verbose_name='投稿状态')
    created = models.DateTimeField(auto_now_add=True, verbose_name='投稿时间')

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return '{0}收录了{1}'.format(self.topic.name, self.article.id)

