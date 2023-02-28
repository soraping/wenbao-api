#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:28
# @Name    : user_role.py
# @email   : 541251250@qq.com
# @Author  : caoping

from src.models.base import BaseModel
from peewee import (
    IntegerField,
    PrimaryKeyField,
    CharField
)


class UserModel(BaseModel):
    """
    用户信息表
    """
    id = PrimaryKeyField()
    username = CharField(unique=True, max_length=20, verbose_name='username')
    password = CharField(max_length=50, verbose_name='user password')
    salt = CharField(max_length=16, verbose_name='password salt')
    age = IntegerField(null=True, verbose_name='user age')
    avatar = CharField(null=True, max_length=100, verbose_name='user avatar')
    mobile = CharField(null=True, unique=True, max_length=20, verbose_name='user mobile')

    class Meta:
        table_name = 'user'
