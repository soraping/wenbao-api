#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:28
# @Name    : user_role.py
# @email   : 541251250@qq.com
# @Author  : caoping

from peewee import (
    PrimaryKeyField,
    ForeignKeyField
)
from .users import UserModel
from .roles import RoleModel
from .base import BaseModel


class UserRoleModel(BaseModel):
    """
    用户角色关系表，多对多
    """
    id = PrimaryKeyField()
    user = ForeignKeyField(model=UserModel, null=True, on_delete='SET NULL', verbose_name='user id')
    role = ForeignKeyField(model=RoleModel, null=True, on_delete='SET NULL', verbose_name='role id')

    class Meta:
        table_name = 'user_roles'
