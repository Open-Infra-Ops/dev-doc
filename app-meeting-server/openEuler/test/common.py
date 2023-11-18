# -*- coding: utf-8 -*-
# @Time    : 2023/11/14 16:37
# @Author  : Tom_zc
# @FileName: common.py
# @Software: PyCharm
from app_meeting_server.utils.common import encrypt_openid, refresh_token_and_refresh_token
from openeuler.models import User, Group


def format_accss_token(token):
    return "Bearer {}".format(token)


def create_group(group_name):
    return Group.objects.create(group_name=group_name)


def get_user(username):
    user = User.objects.get(nickname=username)
    access_token, _ = refresh_token_and_refresh_token(user)
    return format_accss_token(access_token), user


def create_user(username="username", openid="openid"):
    encrypt_openid_str = encrypt_openid(openid)
    user = User.objects.create(
        nickname=username,
        avatar="https://xxxxxxx",
        openid=encrypt_openid_str,
        level=1,
        activity_level=1
    )
    access_token, refresh_token = refresh_token_and_refresh_token(user)
    access_token = format_accss_token(access_token)
    return access_token, refresh_token, user


def create_meetings_sponsor_user(username="username", openid="openid"):
    encrypt_openid_str = encrypt_openid(openid)
    user = User.objects.create(
        nickname=username,
        avatar="https://xxxxxxx",
        openid=encrypt_openid_str,
        level=2
    )
    access_token, _ = refresh_token_and_refresh_token(user)
    return format_accss_token(access_token), user


def create_meeting_admin_user(username="username", openid="openid"):
    encrypt_openid_str = encrypt_openid(openid)
    user = User.objects.create(
        nickname=username,
        avatar="https://xxxxxxx",
        openid=encrypt_openid_str,
        level=3
    )
    access_token, _ = refresh_token_and_refresh_token(user)
    return format_accss_token(access_token), user


def create_activity_sponsor_user(username="username", openid="openid"):
    encrypt_openid_str = encrypt_openid(openid)
    user = User.objects.create(
        nickname=username,
        avatar="https://xxxxxxx",
        openid=encrypt_openid_str,
        activity_level=2
    )
    access_token, _ = refresh_token_and_refresh_token(user)
    return format_accss_token(access_token), user


def create_activity_admin_user(username="username", openid="openid"):
    encrypt_openid_str = encrypt_openid(openid)
    user = User.objects.create(
        nickname=username,
        avatar="https://xxxxxxx",
        openid=encrypt_openid_str,
        activity_level=3
    )
    access_token, _ = refresh_token_and_refresh_token(user)
    return format_accss_token(access_token), user
