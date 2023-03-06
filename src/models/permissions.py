#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:38
# @Name    : permissions.py
# @email   : 541251250@qq.com
# @Author  : caoping

from peewee import (
    CharField
)
from .base import BaseModel


class PermissionModel(BaseModel):
    """
    权限表
    """
    label = CharField(max_length=20, verbose_name='permission name', help_text="权限名")
    value = CharField(max_length=20, verbose_name='permission value', help_text="权限Key")

    class Meta:
        table_name = 'permissions'
