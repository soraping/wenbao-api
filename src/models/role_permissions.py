#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:52
# @Name    : role_permissions.py
# @email   : 541251250@qq.com
# @Author  : caoping

from peewee import (
    ForeignKeyField
)
from .roles import RoleModel
from .base import BaseModel
from .permissions import PermissionModel


class RolePermissionModel(BaseModel):
    """
    角色权限关系表
    """
    role = ForeignKeyField(model=RoleModel, null=True, on_delete='CASCADE', verbose_name='role id')
    permission = ForeignKeyField(model=PermissionModel, null=True, on_delete='SET NULL', verbose_name='permission id')

    class Meta:
        table_name = 'role_permissions'
