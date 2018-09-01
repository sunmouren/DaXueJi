from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from actions.utils import create_action
from utils.check import check_is_request_owner

from .forms import ArticleForm
from .models import Article


class ArticleListView(View):
    """
    文章列表，后面可利用推荐算法推荐相关文章
    """
    def get(self, request):
        articles = Article.objects.all()
        # 分页
        paginator = Paginator(articles, 10)
        page = request.GET.get('page')
        try:
            p_articles = paginator.page(page)
        except PageNotAnInteger:
            p_articles = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            p_articles = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-article-list-ajax.html', {'articles': p_articles})

        # 文章数
        article_count = articles.count()
        # 当前页面信息
        main_top_info = '推荐文章'
        return render(request, 'public-article-list.html', {
            'articles': p_articles,
            'count': article_count,
            'main_top_info': main_top_info
        })


class ArticleDetailView(View):
    """
    文章详情视图
    """
    def get(self, request, article_id):

        article = get_object_or_404(Article, id=int(article_id))
        # 获取文章最近评论
        comments = article.comments.all().order_by('-created')
        comment_count = comments.count()
        paginator = Paginator(comments, 10)
        page = request.GET.get('page')
        try:
            recent_comments = paginator.page(page)
        except PageNotAnInteger:
            recent_comments = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            recent_comments = paginator.page(paginator.num_pages)

        # 如果是ajax则加载评论
        if request.is_ajax():
            return render(request, 'comments-ajax.html', {'recent_comments': recent_comments})

        # +1文章浏览数，那么问题来了，why  write it here?
        # 因为前面的ajax 加载comments时会增加。
        article.view_count_increase()
        return render(request, 'article-detail.html', {
            'article': article,
            'recent_comments': recent_comments,
            'comment_count': comment_count,
        })


class LikeArticleAjax(LoginRequiredMixin, View):
    """
    采用Ajax进行喜欢文章操作
    允许条件: 用户已登录和只能通过post方式提交
    """
    def post(self, request):
        article_id = request.POST.get('aid', None)
        action = request.POST.get('action', None)
        if article_id and action:
            try:
                article = Article.objects.get(id=article_id)
                if action == 'like':
                    article.user_like.add(request.user)
                else:
                    article.user_like.remove(request.user)
                return JsonResponse({'msg': 'ok'})
            except Article.DoesNotExist:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddArticleView(LoginRequiredMixin, View):
    """
    添加文章视图
    """
    def get(self, request):
        article_form = ArticleForm()
        return render(request, 'add-article.html', {'article_form': article_form})

    def post(self, request):
        article_form = ArticleForm(data=request.POST, files=request.FILES)
        print(request.FILES)
        if article_form.is_valid():
            try:
                new_article = article_form.save(commit=False)
                new_article.author = request.user
                new_article.save()
                create_action(request.user, 'new_article', new_article)
                return HttpResponseRedirect(reverse('index'))
            except BaseException as e:
                print('文章保存失败信息{0}'.format(e))
        return render(request, 'add-article.html', {
            'article_form': article_form,
            'edit_status': 'ko'
        })


class EditArticleView(LoginRequiredMixin, View):
    """
    编辑文章视图
    允许条件: 已登录，所要编辑的文章和当前请求者匹配
    """
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=int(article_id))
        check_is_request_owner(request, article.author)
        article_form = ArticleForm(instance=article)
        return render(request, 'edit-article.html', {
            'article': article,
            'article_form': article_form
        })

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=int(article_id))
        check_is_request_owner(request, article.author)
        article_form = ArticleForm(instance=article, data=request.POST, files=request.FILES)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse('writing:article_detail', args=[int(article_id)]))
        return render(request, 'edit-article.html', {
            'article': article,
            'article_form': article_form,
            'edit_status': 'ko'
        })


class DeleteArticleAjax(LoginRequiredMixin, View):
    """
    删除文章视图
    允许条件：已登录，所要删除的文章和当前请求者匹配, 且只能是POST方式
    """
    def post(self, request):
        article_id = request.POST.get('aid', None)
        print(article_id)
        if article_id:
            try:
                article = Article.objects.get(id=int(article_id))
                check_is_request_owner(request, article.author)
                article.delete()
                return JsonResponse({'msg': 'ok'})
            except Article.DoesNotExist:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})










