# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/18 22:34
@desc: users app 表单
"""
from django import forms
from django.forms import ModelForm

from .models import UserProfile


class LoginForm(forms.Form):
    """
    登录验证表单
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """
    注册验证表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)


class ForgetPwdForm(forms.Form):
    """
    忘记密码表单
    """
    email = forms.EmailField(required=True)


class UserProfileForm(ModelForm):
    """
    修改个人信息
    """
    class Meta:
        model = UserProfile
        fields = ('avatar', 'signature', 'nickname', 'gender')


class ResetPwdForm(forms.Form):
    """
    重置密码
    """
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
