import time
import requests
from PIL import Image
from io import BytesIO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


from topics.models import Topic
from utils.email_send import send_register_email
from utils.check import check_is_request_owner
from actions.utils import create_action
from actions.models import Action


from .models import UserProfile, EmailVerifyRecord, FollowUser, FollowTopic
from .forms import LoginForm, RegisterForm, UserProfileForm, ForgetPwdForm, ResetPwdForm
from .wb_oauth import OAuthWB


class LoginView(View):
    """
    登录视图
    """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 表单实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象，反之返回None
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 只有注册激活才能登录
                if user.is_active:
                    login(request, user)
                    request.session['active_status'] = ''
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '该用户还没有进行邮箱链接激活', 'login_form': login_form})
            else:
                # 只有当用户名或密码不存在时，才返回错误信息到前端
                print(login_form.errors)
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
            return render(request, 'login.html', {'login_form': login_form})


class CustomBackend(ModelBackend):
    """
    增加邮箱登录
    继承ModelBackend类，覆盖authenticate方法, 增加邮箱认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 使用get是因为不希望用户存在两个, Q：使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 判断密码是否匹配时，django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有check_password(self, raw_password)方法
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        """
        传给模板的上下文msg中
        0 ： 发送邮箱验证码失败
        1 : 用户已存在
        -1 ： 用户提交信息不合法
        """
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            pass_word = request.POST.get('password', None)
            # 判断用户是否存在，如果已存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html',
                              {'register_form': register_form, 'msg': '1'})

            # 实例化一个UserProfile对象，并进行相应的赋值
            user_profile = UserProfile(username=user_name, email=user_name)
            # 需要邮箱验证才能激活
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # 通过邮箱发送注册验证
            try:
                send_register_email(user_name, 'register')
            except BaseException as e:
                user_profile.delete()
                return render(request, 'register.html', {'register_form': register_form,
                                                         'msg': '0'})
            # 重定向不能直接通过context传信息，可以通过session进行传递简单信息
            request.session['active_status'] = ''
            request.session['send_email_status'] = 'ok'
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'register.html', {'register_form': register_form,
                                                     'msg': '-1'})


class ActiveUserView(View):
    """
    激活用户视图
    """
    def get(self, request, active_code):
        # 查询邮箱验证码记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # # 激活成功后删除对应的激活吗
                # record.delete()
                # 置空注册时重定向遗留下的send_email_status
                request.session['send_email_status'] = ''
                request.session['active_status'] = 'ok'
                # 激活成功重定向到登录页面
                return HttpResponseRedirect(reverse('users:login'))
        else:
            # 验证码不对的时候跳转到激活失败页面
            return render(request, 'active-fail.html')


class LogoutView(View):
    """
    用户登出视图
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ForgetPwdView(View):
    """
    忘记密码视图
    """
    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request, 'forget-pwd.html', {
            'forget_pwd_form': forget_pwd_form
        })

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get('email', None)
            try:
                send_register_email(email, 'forget')
            except BaseException as e:
                print(e)
                return render(request, 'forget-pwd.html', {'send_status': 'ko'})
            return render(request, 'forget-pwd.html', {'send_status': 'ok'})
        return render(request, 'forget-pwd.html', {'send_status': 'ko'})


class GetResetPwdView(View):
    """
    这里只是获取重置密码视图，重置密码具体逻辑另写，主要是因为active_code的存在，如果直接写会要求传active_code
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'reset-pwd.html', {'email': email})
        return render(request, 'active-fail.html')


class PostResetPwdView(View):
    """
    提交重置密码视图
    """
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        email = request.POST.get('email', '')
        if reset_pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'reset-pwd.html', {
                    'email': email,
                    'reset_status': 'ko'
                })
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'reset-pwd.html', {'reset_status': 'ok'})
        return render(request, 'reset-pwd.html', {
            'email': email,
            'reset_pwd_form': reset_pwd_form
        })


class RecommendAuthorListView(View):
    """
    推荐用户列表视图,
    """
    def get(self, request):
        # 记录current_page, 为了判断a标签激活状态
        current_page = 'recommend_authors'
        # demo阶段，暂时获取前15名老用户, 排除已经登录的自己和已经关注的粉丝
        recommend_authors = UserProfile.objects.exclude(id=request.user.id).exclude(is_active=False)\
            .order_by('date_joined')
        # if request.user.is_authenticated:
        #     following_ids = request.user.following_user.values_list('id', flat=True)
        #     if following_ids:
        #         suggested_authors = suggested_authors.exclude(id__in=following_ids)
        return render(request, 'author.html', {
            'recommend_authors': recommend_authors[:15],
            'current_page': current_page
        })


class UserHomePageView(View):
    """
    user homepage
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        articles = user.articles.all()[:5]
        comments = user.user_comments.all().filter(parent=None)[:5]
        followers = user.followers_user.all()[:5]
        actions = get_user_actions(user=user)[:5]
        if request.user == user:
            return render(request, 'user-default.html', {
                'user_default': user,
                'articles': articles,
                'comments': comments,
                'followers': followers,
                'actions': actions
            })
        return render(request, 'user-other.html', {
            'user_other': user,
            'articles': articles,
            'comments': comments,
            'followers': followers,
            'actions': actions
        })


class FollowUserAjax(LoginRequiredMixin, View):
    """
    采用Ajax进行用户关注操作, y
    允许条件: 用户已登录和只能通过post方式提交
    """
    def post(self, request):
        user_id = request.POST.get('uid', None)
        action = request.POST.get('action', None)
        if user_id and action:
            try:
                user = UserProfile.objects.get(id=user_id)
                # 前端避免不了关注自己，那么就就来接受第二道关卡吧，我就不信了。
                if request.user == user:
                    return JsonResponse({'msg': 'ko'})

                if action == 'follow':
                    FollowUser.objects.get_or_create(user_from=request.user,
                                                     user_to=user)
                else:
                    FollowUser.objects.filter(user_from=request.user,
                                              user_to=user).delete()
                return JsonResponse({'msg': 'ok'})
            except UserProfile.DoesNotExist:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class FollowTopicAjax(LoginRequiredMixin, View):
    """
    采用Ajax进行专题关注操作
    允许条件: 用户已登录和只能通过post方式提交
    """
    def post(self, request):
        topic_id = request.POST.get('tid', None)
        action = request.POST.get('action', None)
        if topic_id and action:
            try:
                topic = Topic.objects.get(id=topic_id)
                if action == 'follow':
                    FollowTopic.objects.get_or_create(user=request.user, topic=topic)
                    create_action(request.user, 'follow_topic', topic)
                else:
                    FollowTopic.objects.filter(user=request.user, topic=topic).delete()
                return JsonResponse({'msg': 'ok'})
            except Topic.DoesNotExist:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class UserArticleListView(View):
    """
    用户文章列表详情
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        articles = user.articles.all()
        # 分页
        paginator = Paginator(articles, 10)
        page = request.GET.get('page')
        try:
            user_articles = paginator.page(page)
        except PageNotAnInteger:
            user_articles = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            user_articles = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-article-list-ajax.html', {'articles': user_articles})

        # 当前页面信息
        main_top_info = '我的文章列表' if request.user == user else 'TA的文章列表'
        # 文章数
        article_count = len(articles)
        return render(request, 'public-article-list.html', {
            'articles': user_articles,
            'count': article_count,
            'main_top_info': main_top_info
        })


class UserCommentsListView(View):
    """
    用户评论列表详情
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        comments = user.user_comments.all().filter(parent=None)
        # 分页
        paginator = Paginator(comments, 10)
        page = request.GET.get('page')
        try:
            user_comments = paginator.page(page)
        except PageNotAnInteger:
            user_comments = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            user_comments = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-comment-list-ajax.html', {'articles': user_comments})

        # 当前页面信息
        main_top_info = '我的评论列表' if request.user == user else 'TA的评论列表'
        # 文章数
        comment_count = len(comments)
        return render(request, 'public-comment-list.html', {
            'comments': user_comments,
            'comment_count': comment_count,
            'main_top_info': main_top_info
        })


class UserFollowerListView(View):
    """
    用户粉丝列表
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        followers = user.followers_user.all()
        # 分页
        paginator = Paginator(followers, 10)
        page = request.GET.get('page')
        try:
            user_followers = paginator.page(page)
        except PageNotAnInteger:
            user_followers = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            user_followers = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-user-list-ajax.html', {'users': user_followers})

        # 当前页面信息
        main_top_info = '我的粉丝' if request.user == user else 'TA的粉丝'
        # 分数数
        follower_count = len(followers)
        return render(request, 'public-user-list.html', {
            'users': user_followers,
            'user_count': follower_count,
            'main_top_info': main_top_info
        })


class UserFollowingUserListView(View):
    """
    用户关注的用户列表
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        following_users = user.following_user.all()
        # 分页
        paginator = Paginator(following_users, 10)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            users = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-user-list-ajax.html', {'users': users})

        # 当前页面
        current_page = 'following_user'

        # 当前页面信息
        main_top_info = '我的关注' if request.user == user else 'TA的关注'
        # 分数数
        user_count = len(following_users)
        return render(request, 'user-following-list.html', {
            'user_object': user,
            'users': users,
            'count': user_count,
            'main_top_info': main_top_info,
            'current_page': current_page
        })


class UserFollowingTopicListView(View):
    """
    用户关注的话题列表
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        following_topics = user.following_topic.all()
        # 分页
        paginator = Paginator(following_topics, 10)
        page = request.GET.get('page')
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            topics = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-topic-list-ajax.html', {'topics': topics})

        # 当前页面
        current_page = 'following_topic'

        # 当前页面信息
        main_top_info = '我的关注' if request.user == user else 'TA的关注'
        # 分数数
        user_count = len(following_topics)
        return render(request, 'user-following-list.html', {
            'user_object': user,
            'topics': topics,
            'count': user_count,
            'main_top_info': main_top_info,
            'current_page': current_page
        })


class UserActionListView(View):
    """
    用户动态列表
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        user_actions = get_user_actions(user=user)
        # 分页
        paginator = Paginator(user_actions, 10)
        page = request.GET.get('page')
        try:
            actions = paginator.page(page)
        except PageNotAnInteger:
            actions = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            actions = paginator.page(paginator.num_pages)

        if request.is_ajax():
            return render(request, 'public-actions-list-ajax.html', {'actions': actions})

        # 当前页面信息
        main_top_info = '我的动态' if request.user == user else 'TA的动态'
        # 分数数
        action_count = len(user_actions)
        return render(request, 'public-action-list.html', {
            'actions': actions,
            'count': action_count,
            'main_top_info': main_top_info,
        })


class EditUserProfileView(LoginRequiredMixin, View):
    """
    编辑用户个人信息
    """
    def get(self, request, user_id):
        user = self.get_user(request, user_id)
        user_profile_form = UserProfileForm(instance=user)
        return render(request, 'profile.html', {
            'user': user,
            'user_profile_form': user_profile_form
        })

    def post(self, request, user_id):
        user = self.get_user(request, user_id)
        user_profile_form = UserProfileForm(instance=user, data=request.POST, files=request.FILES)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return HttpResponseRedirect(user.get_absolute_url())
        return render(request, 'profile.html', {
            'user': user,
            'user_profile_form': user_profile_form,
            'edit_status': 'ko'
        })

    def get_user(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        check_is_request_owner(request, user)
        return user


def get_user_actions(user):
    """
    获取用户的活动，并检查action实例的target是否存在，不存在，则删除对应的action实例
    :param user:
    :return:
    """
    actions = [action if action.target else action.delete() for action in Action.objects.filter(user=user)]
    return actions


def oauth_weibo(request):
    """
    微博授权页面登录
    :param request:
    :return:
    """
    url = 'https://api.weibo.com/oauth2/authorize?client_id={0}&redirect_uri={1}'.format(settings.WEIBO_APP_ID, settings.WEIBO_REDIRECT_URI)
    return HttpResponseRedirect(url)


def weibo_login(request):
    code = request.GET.get('code', None)
    sina_weibo = OAuthWB(settings.WEIBO_APP_ID, settings.WEIBO_APP_KEY, settings.WEIBO_REDIRECT_URI)
    user_info = sina_weibo.get_access_token(code)
    # 防止还没请求到token就进行下一步
    time.sleep(0.1)
    user = UserProfile.objects.filter(openid=user_info['uid']).first()
    if user:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        new_user_info = sina_weibo.get_user_info(user_info)
        new_user = UserProfile()
        new_user.openid = new_user_info['id']
        new_user.username = new_user_info['name']
        new_user.nickname = new_user_info['name']
        new_user.signature = new_user_info['description']
        new_user.avatar = get_user_avatar(img_src=new_user_info['profile_image_url'])

        # 注意这里保存出错
        new_user.save()
        login(request, new_user)
        return HttpResponseRedirect(reverse('index'))


def get_user_avatar(img_src):
    """
    处理第三方返回的头像
    :param img_url:
    :return:
    """
    # 获取图片名字
    avatar_name = img_src.split('/')[-1]
    # 通过第三方返回的头像地址加载图片
    response = requests.get(img_src)
    avatar_io = BytesIO(response.content)
    if response.status_code == 200:
        image = Image.open(avatar_io)
        # 转换为 InMemoryUploadedFile 以便于可以保存到数据库中
        avatar_file = InMemoryUploadedFile(file=avatar_io, field_name=None, name=avatar_name,
                                           content_type=image.format, size=image.size, charset=None)
        return avatar_file
    else:
        return None