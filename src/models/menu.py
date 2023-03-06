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
    # 上级ID
    parent = IntegerField(verbose_name='menu parent menu', null=True)
    # 菜单名称/按钮名称
    name = CharField(max_length=20, verbose_name='menu title')
    # 图标
    icon = CharField(null=True, max_length=64, verbose_name="菜单图标", help_text="菜单图标")
    # 状态
    status = IntegerField(choices=((0, '删除'), (1, '正常')), verbose_name='menu status', default=1)
    type = IntegerField(null=True, choices=((0, "目录/一级菜单"), (1, "菜单/具体页面"), (2, "按钮")), verbose_name="是否目录", default=1)

    key = CharField(null=True, max_length=20, verbose_name='menu key')
    # 权限标示 PermissionModel
    permission = CharField(max_length=20, verbose_name='menu auth')
    # 路由路径
    path = CharField(null=True, max_length=100, verbose_name='menu path', help_text="路由地址")
    # 重定向地址
    redirect = CharField(null=True, max_length=128, verbose_name="重定向地址", help_text="重定向地址")
    # 对应前端模块名路径 /dashboard/console/console
    component = CharField(null=True, max_length=100, verbose_name='view component')
    # 排序
    sort = IntegerField(null=True, verbose_name="排序", default=0)

    class Meta:
        table_name = 'menu'
