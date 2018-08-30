from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from writing.models import Article
from comments.models import Comment
from users.models import FollowTopic
from utils.check import check_is_request_owner

from .models import Topic, RecordArticle


class HotTopicListView(View):
    """
    热门专题视图
    """
    def get(self, request):
        # 记录current_page, 为了判断a标签激活状态
        current_page = 'hot_topics'
        hot_topics = Topic.objects.all()
        return render(request, 'topic-hots.html', {
            'hot_topics': hot_topics,
            'current_page': current_page
        })


class TopicDetailView(View):
    """
    专题详情视图
    """
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=int(topic_id))
        articles = get_topic_articles(topic=topic, is_all=False)
        # 获取专题收录文章的最新评论
        comments = get_topic_articles_comments(articles=articles, is_all=False)
        # 获取最近关注的粉丝
        followers = get_topic_followers(topic=topic, is_all=False)
        return render(request, 'topic-detail.html', {
            'topic': topic,
            'articles': articles,
            'comments': comments,
            'followers': followers
        })


class RecordArticleAjax(LoginRequiredMixin, View):
    """
    投稿文章
    允许条件：用户已经登录，只能投稿自己的文章，POST方式
    """
    def post(self, request):
        article_id = request.POST.get('aid', None)
        topic_id = request.POST.get('tid', None)
        action = request.POST.get('action', None)
        if article_id and topic_id and action:
            try:
                article = Article.objects.get(id=int(article_id))
                topic = Topic.objects.get(id=int(topic_id))
                check_is_request_owner(request, article.author)
                if action == 'record':
                    RecordArticle.objects.get_or_create(article=article, topic=topic)
                else:
                    RecordArticle.objects.filter(article=article, topic=topic).delete()
                return JsonResponse({'msg': 'ok'})
            except (Article.DoesNotExist, Topic.DoesNotExist) as e:
                print("投稿异常信息:{0}".format(e))
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class CanRecordArticleAJax(LoginRequiredMixin, View):
    """
    获取用户要投稿的文章
    """
    def get(self, request):
        topic_id = request.GET.get('tid')
        print(topic_id)
        if topic_id:
            topic = get_object_or_404(Topic, id=int(topic_id))
            recorded_articles = topic.articles.filter(author=request.user)
            print(recorded_articles)
            article_ids = [article.id for article in recorded_articles]
            articles = Article.objects.filter(author=request.user).exclude(id__in=article_ids)
            print(articles)
            return render(request, 'modal-article-ajax.html', {
                'can_record_articles': articles
            })
        return render(request, 'modal-article-ajax.html', {
            'can_record_articles': []
        })


class TopicArticleListView(View):
    """
    专题收录文章列表详情
    """
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=int(topic_id))
        articles = get_topic_articles(topic=topic, is_all=True)
        paginator = Paginator(articles, 10)
        page = request.GET.get('page')
        try:
            topic_articles = paginator.page(page)
        except PageNotAnInteger:
            topic_articles = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            topic_articles = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-article-list-ajax.html', {'articles': topic_articles})
        # 当前页面信息
        main_top_info = '收录文章列表'
        # 收录文章数
        article_count = len(articles)
        return render(request, 'public-article-list.html', {
            'articles': topic_articles,
            'count': article_count,
            'main_top_info': main_top_info
        })


class TopicArticleCommentListView(View):
    """
    专题收录文章评论列表列表详情
    """
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=int(topic_id))
        articles = get_topic_articles(topic=topic, is_all=True)
        comments = get_topic_articles_comments(articles=articles, is_all=True)
        # 分页
        paginator = Paginator(comments, 10)
        page = request.GET.get('page')
        try:
            topic_comments = paginator.page(page)
        except PageNotAnInteger:
            topic_comments = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            topic_comments = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-comment-list-ajax.html', {'articles': topic_comments})
        # 当前页面信息
        main_top_info = '收录文章最新评论'
        # 评论数
        comment_count = len(articles)
        return render(request, 'public-comment-list.html', {
            'comments': topic_comments,
            'comment_count': comment_count,
            'main_top_info': main_top_info
        })


class TopicFollowerListView(View):
    """
    专题粉丝列表
    """
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=int(topic_id))
        followers = get_topic_followers(topic=topic, is_all=True)
        # 分页
        paginator = Paginator(followers, 10)
        page = request.GET.get('page')
        try:
            topic_followers = paginator.page(page)
        except PageNotAnInteger:
            topic_followers = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            topic_followers = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-user-list-ajax.html', {'users': topic_followers})

        # 当前页面信息
        main_top_info = '关注的人'
        # 分数数
        follower_count = len(followers)
        return render(request, 'public-user-list.html', {
            'users': topic_followers,
            'user_count': follower_count,
            'main_top_info': main_top_info
        })


def get_topic_articles(topic, is_all=False):
    """
    获取专题收录的文章 按时间-created排序（默认返回）
    :param topic: 专题
    :param is_all: 是否返回全部
    :return:
    """
    records = RecordArticle.objects.filter(topic=topic)
    articles = [record.article for record in records]
    return articles if is_all else articles[:5]


def get_topic_articles_comments(articles, is_all=False):
    """
    获取专题收录文章的最新评论
    :param articles: 收录的文章
    :param is_all: 是否为返回全部
    :return:
    """
    article_ids = [article.id for article in articles]
    comments = Comment.objects.filter(article_id__in=article_ids).filter(parent=None)
    return comments if is_all else comments[:5]


def get_topic_followers(topic, is_all=False):
    """
    获取专题粉丝
    :param topic:
    :param is_all:
    :return:
    """
    follow_topic_records = FollowTopic.objects.filter(topic=topic)
    users = [record.user for record in follow_topic_records]
    return users if is_all else users[:5]
