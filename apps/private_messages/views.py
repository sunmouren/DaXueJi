from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from users.models import UserProfile
from utils.check import check_is_request_owner

from .models import PrivateMessage


class PrivateMessageListView(LoginRequiredMixin, View):
    """
    用户私信列表视图
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        # 检查是否和当前请求者为同一个人
        check_is_request_owner(request, user)
        # 当前用户发起的私信列表
        sent_messages = user.sent_messages.filter(parent=None)
        # 当前用户接收的私信列表
        received_messages = user.received_messages.filter(parent=None)
        # 合并私信
        private_messages = list(sent_messages) + list(received_messages)
        # 按私信时间排序
        private_messages = sorted(private_messages, key=lambda pm: pm.created)

        return render(request, 'private-message-list.html', {
            'private_messages': private_messages
        })


class PrivateMessageChatView(LoginRequiredMixin, View):
    """
    私信详情视图，也就是聊天界面
    """
    def get(self, request, user_to_id):
        user_to = get_object_or_404(UserProfile, id=int(user_to_id))
        descendants = []
        parent_pm = get_parent_pm(request, user_to)
        if parent_pm:
            if request.user != parent_pm.user_from and request.user != parent_pm.user_to:
                raise Http404
            descendants = parent_pm.get_family()

        return render(request, 'private-message-chat.html', {
            'descendants': descendants,
            'user_to': user_to,
        })


def get_parent_pm(request, user_to):
    """
    :param request:
    :param user_to:
    :return: 理论上只存在一个parent root
    """
    had_sent_pms = PrivateMessage.objects.filter(user_from=request.user, user_to=user_to, parent=None)
    had_received_pms = PrivateMessage.objects.filter(user_from=user_to, user_to=request.user, parent=None)
    had_pms = list(had_sent_pms) + list(had_received_pms)
    had_pms = sorted(had_pms, key=lambda pm: pm.created)
    return had_pms[0] if had_pms else None


class AddPrivateMessageAJax(LoginRequiredMixin, View):
    """
    添加私信
    """
    def post(self, request):
        user_to_id = request.POST.get('uid', None)
        content = request.POST.get('content', None)
        if user_to_id and content:
            try:
                user_to = UserProfile.objects.get(id=int(user_to_id))
                new_pm = PrivateMessage(user_from=request.user, user_to=user_to, content=content)
                parent_pm = get_parent_pm(request, user_to)
                if parent_pm:
                    new_pm.parent = parent_pm
                new_pm.save()
                return JsonResponse({'msg': 'ok'})
            except (UserProfile.DoesNotExist, BaseException) as e:
                print("私信异常信息:{0}".format(e))
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})