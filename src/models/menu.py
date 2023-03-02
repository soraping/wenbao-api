#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 09:49
# @Name    : menu.py
# @email   : 541251250@qq.com
# @Author  : caoping

from peewee import (
    CharField,
    IntegerField
)
from .base import BaseModel


class MenuModel(BaseModel):
    """
    动态菜单
    """
    # 上级菜单目录
    parent = IntegerField(verbose_name='menu parent menu', null=True)
    # 标题
    name = CharField(max_length=20, verbose_name='menu title')
    # 图标
    icon = CharField(null=True, max_length=64, verbose_name="菜单图标", help_text="菜单图标")
    # 状态
    status = IntegerField(choices=((0, '删除'), (1, '正常')), verbose_name='menu status', default=1)
    # 是否目录
    type = IntegerField(choices=((0, "目录"), (1, "菜单")), verbose_name="是否目录", default=1)

    key = CharField(null=True, max_length=20, verbose_name='menu key')
    # 权限标示 PermissionModel
    permission = CharField(max_length=20, verbose_name='menu auth')
    # 路由路径
    path = CharField(max_length=100, verbose_name='menu path', help_text="路由地址")
    # 重定向地址
    redirect = CharField(max_length=128, verbose_name="重定向地址", null=True, help_text="重定向地址")
    # 对应前端模块名路径 /dashboard/console/console
    component = CharField(max_length=100, verbose_name='view component')

    class Meta:
        table_name = 'menu'
