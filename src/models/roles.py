#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:28
# @Name    : user_role.py
# @email   : 541251250@qq.com
# @Author  : caoping

from enum import Enum
from peewee import (
    CharField,
    PrimaryKeyField
)
from src.models.base import BaseModel


class RoleTypeEnum(Enum):
    """
    角色类型
    """
    # 管理员
    ADMIN = 'ADMIN'
    # 员工
    EMPLOYEE = 'EMPLOYEE'

    # 普通用户
    USER = 'USER'
    # 自定义
    CUSTOM = 'CUSTOM'


class RoleModel(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=20, verbose_name='role name')
    type = CharField(max_length=20, verbose_name='role type')

    class Meta:
        table_name = 'roles'