from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings

from topics.models import Topic


class UserProfile(AbstractUser):
    gender_choices = (('male', '男'), ('female', '女'))
    nickname = models.CharField(max_length=30, blank=True,
                                null=True, verbose_name='昵称')
    signature = models.CharField(max_length=128, blank=True,
                                 null=True, verbose_name='个性签名', default='这家伙很懒，什么都没有留下！')
    gender = models.CharField(verbose_name='性别', max_length=10,
                              choices=gender_choices, default='female')
    following_user = models.ManyToManyField('self', through='FollowUser',
                                            related_name='followers_user',
                                            symmetrical=False)
    following_topic = models.ManyToManyField(Topic, through='FollowTopic',
                                             related_name='followers_topic',
                                             symmetrical=False)
    avatar = models.ImageField(upload_to='image/%Y%m',
                               default='image/default.jpg', verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    # 获取用户绝对路径
    def get_absolute_url(self):
        return reverse('users:user_homepage', args=[self.id])

    # 便于前端是显示username还是nickname
    def get_username_or_nickname(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username

    # 获取文章列表
    def get_article_list(self):
        return reverse('users:user_articles', args=[self.id])

    # 获获取评论过的列表
    def get_comment_list(self):
        return reverse('users:user_comments', args=[self.id])

    # 获取粉丝列表
    def get_follower_list(self):
        return reverse('users:user_followers', args=[self.id])

    # 获取关注的用户列表
    def get_following_user_list(self):
        return reverse('users:user_following_users', args=[self.id])

    # 获取关注的专题列表
    def get_following_topic_list(self):
        return reverse('users:user_following_topics', args=[self.id])

    # 获取用户动态列表
    def get_action_list(self):
        return reverse('users:user_actions', args=[self.id])

    # 获取用户私信列表
    def get_private_message_list(self):
        return reverse('private_messages:pm_list', args=[self.id])

    # 获取用户个人信息并编辑
    def get_profile(self):
        return reverse('users:edit_profile', args=[self.id])

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证表
    """
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码')
    )
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=send_choices, max_length=10)
    send_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class FollowUser(models.Model):
    """
    关注用户中间模型（这个模型可以添加额外的字段，例如: 创建时间字段）
    关于中间模型：原来些关系管理器的方法将不可用，例如：add()，create()以及remove()。
    你需要创建或删除中介模型（intermediate model）的实例来代替。
    """
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = '关注用户'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return '{0} 关注了 {1}用户'.format(self.user_from, self.user_to)


class FollowTopic(models.Model):
    """
    用户关注专题中间模型
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='rel_user_set')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='rel_topic_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = '关注专题'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return '{0} 关注了 {1}话题'.format(self.user, self.topic)


