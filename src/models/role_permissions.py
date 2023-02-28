#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:52
# @Name    : role_permissions.py
# @email   : 541251250@qq.com
# @Author  : caoping

from peewee import (
    PrimaryKeyField,
    ForeignKeyField
)
from .roles import RoleModel
from .base import BaseModel
from .permissions import Permissions


class RolePermissions(BaseModel):
    """
    角色权限关系表
    """
    id = PrimaryKeyField()
    role = ForeignKeyField(model=RoleModel, null=True, on_delete='SET NULL', verbose_name='role id')
    permission = ForeignKeyField(model=Permissions, null=True, on_delete='SET NULL', verbose_name='permission id')

    class Meta:
        table_name = 'role_permissions'
