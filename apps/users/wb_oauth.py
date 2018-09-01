# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/1 11:29
@desc: 微博第三方登录
"""

import requests
import json


class OAuthWB:
    """
    微博认证
    """
    def __init__(self, client_id, client_key, redirect_url):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def get_access_token(self, code):
        """
        获取用户token和uid（openid)
        :param code:
        :return:
        """
        url = "https://api.weibo.com/oauth2/access_token"

        querystring = {
            "client_id": self.client_id,
            "client_secret": self.client_key,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_url
        }
        response = requests.request("POST", url, params=querystring)
        return json.loads(response.text)

    def get_user_info(self, access_token_data):
        """
        获取用户简单相关信息
        :param access_token_data:
        :return:
        """
        url = "https://api.weibo.com/2/users/show.json"

        querystring = {
            "uid": access_token_data['uid'],
            "access_token": access_token_data['access_token']
        }

        response = requests.request("GET", url, params=querystring)

        return json.loads(response.text)
