#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:38
# @Name    : permissions.py
# @email   : 541251250@qq.com
# @Author  : caoping

from peewee import (
    CharField,
    PrimaryKeyField
)
from .base import BaseModel


class Permissions(BaseModel):
    """
    权限表
    """
    id = PrimaryKeyField()
    label = CharField(max_length=20, verbose_name='permission name')
    value = CharField(max_length=20, verbose_name='permission value')

    class Meta:
        table_name = 'permissions'
