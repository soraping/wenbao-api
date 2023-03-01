from typing import List
from dataclasses import dataclass
from peewee_async import Manager
from sanic import Request as SanicRequest


# @dataclass
# class AuthUser:
#     role: str
#     user_id: str


class Roles:
    role_id: int
    role_name: str
    role_type: str


class Permissions:
    label: str
    value: str


class AuthUser:
    user_id: str
    user_id: int
    token: str
    username: str
    age: int
    avatar: str
    mobile: str
    status: int
    roles: List[Roles]
    permissions: List[Permissions]


class MyContent:
    """
    自定义上下文
    """
    # jwt 会话
    auth_user: AuthUser
    # db
    db: Manager
    # redis
    # mongo


class Request(SanicRequest):
    """
    自定义请求类
    """
    ctx: MyContent
