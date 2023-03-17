#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:28
# @Name    : user_role.py
# @email   : 541251250@qq.com
# @Author  : caoping

from src.models.base import BaseModel
from peewee import (
    IntegerField,
    CharField
)


class UserModel(BaseModel):
    """
    用户信息表
    """
    username = CharField(unique=True, max_length=20, verbose_name='username')
    password = CharField(max_length=50, verbose_name='user password')
    salt = CharField(max_length=16, verbose_name='password salt')
    age = IntegerField(null=True, verbose_name='user age')
    avatar = CharField(null=True, max_length=100, verbose_name='user avatar')
    mobile = CharField(null=True, unique=True, max_length=20, verbose_name='user mobile')
    status = IntegerField(choices=((0, '删除'), (1, '正常'), (2, '锁定')), verbose_name='user status', default=1)
    card_id = CharField(null=True, max_length=50, verbose_name='ID CARD', help_text='身份证', unique=True)
    invite_owner_code = CharField(null=True, max_length=15, verbose_name='owner invite code', help_text='专属邀请码', unique=True)
    inviter_user_id = CharField(null=True, max_length=15, verbose_name='inviter userId', help_text='邀请人ID')
    star = IntegerField(null=True, verbose_name='member level', help_text='会员星级', default=0)


    class Meta:
        table_name = 'user'
