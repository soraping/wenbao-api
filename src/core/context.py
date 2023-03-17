from typing import List
import types
from dataclasses import dataclass
from peewee_async import Manager
from sanic import Request as SanicRequest
from .base import BaseBean


# @dataclass
# class AuthUser:
#     role: str
#     user_id: str

class Session:
    ...


class Roles:
    role_id: int
    role_name: str
    role_type: str


class Permissions:
    label: str
    value: str


class AuthUser(BaseBean):
    user_id: str
    token: str
    username: str
    age: int
    avatar: str
    mobile: str
    status: int
    roles: List[Roles]
    permissions: List[Permissions]

    @classmethod
    def get_user(cls, auth_user):
        cls.user_id = auth_user.get('id')
        cls.username = auth_user.get('username')
        cls.status = auth_user.get('status')
        cls.roles = auth_user.get('roles')
        cls.permissions = auth_user.get('permissions')
        return cls()


class MyContent:
    """
    自定义上下文
    """
    # jwt 会话
    auth_user: AuthUser
    # session
    session: Session
    # db
    db: Manager
    # redis
    # mongo


class Request(SanicRequest):
    """
    自定义请求类
    """
    ctx: MyContent
