"""DaXueJi_Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import notifications.urls

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve


from DaXueJi_Demo.settings import MEDIA_ROOT

from users.models import UserProfile
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('nickname', 'gender', 'avatar', 'signature', 'following_user', 'followers_user')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # # 处理图片显示的url，使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # index
    path('', TemplateView.as_view(template_name='index.html', extra_context={'current_page': ''}), name='index'),
    # users
    path('user/', include('users.urls', namespace='users')),
    # writing
    path('article/', include('writing.urls', namespace='writing')),
    # topics
    path('topic/', include('topics.urls', namespace='topics')),
    # actions
    path('action/', include('actions.urls', namespace='actions')),
    # comments
    path('comment/', include('comments.urls', namespace='comments')),
    # notifications
    path('notification/', include(notifications.urls, namespace='notifications')),
    # private_messages
    path('message/', include('private_messages.urls', namespace='private_messages')),
    # api-auth
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

]
