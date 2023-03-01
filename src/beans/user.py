#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/1 13:55
# @Name    : users.py
# @email   : 541251250@qq.com
# @Author  : caoping

import typing
from dataclasses import dataclass


@dataclass
class RoleClass:
    role_id: int
    role_name: str
    role_type: str


@dataclass
class PermissionClass:
    label: str
    value: str


@dataclass
class UserClass:
    user_id: int
    token: str
    username: str
    age: int
    avatar: str
    mobile: str
    status: int
    roles: typing.List[RoleClass]
    permissions: typing.List[PermissionClass]
