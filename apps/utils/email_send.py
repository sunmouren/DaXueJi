# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/7/19 10:33
@desc: 注册、忘记密码、修改密码，发送邮箱验证
"""

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from DaXueJi_Demo.settings import EMAIL_FROM


def random_str(random_length=8):
    """
    生成随机字符串
    :param random_length:
    :return:
    """
    strs = ''
    # 生成随机字符串可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for _ in range(random_length):
        strs += chars[random.randint(0, length)]
    return strs


def send_register_email(email, send_type="register"):
    """
    发送注册邮箱。
    发送之前要先保存到数据库，到时候查询链接是否存在。
    :param email: 收件人邮箱
    :param send_type:
    :return:
    """
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 将生成的随机code放入链接
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = "Python技术杂货铺注册激活链接"
        email_body = "请点击下面的链接激活您的账号: http://127.0.0.1:8000/{0}/active/{1}".format('user', code)
        # 使用Django内置函数完成邮件发送，四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass

    if send_type == 'forget':
        email_title = "Python技术杂货铺找回密码链接"
        email_body = "请点击下面的链接找回您的密码链接: http://127.0.0.1:8000/{0}/get/reset/{1}".format('user', code)
        # 使用Django内置函数完成邮件发送，四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass


