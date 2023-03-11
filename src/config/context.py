from typing import List
import types
from dataclasses import dataclass
from peewee_async import Manager
from sanic import Request as SanicRequest


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

    @classmethod
    def get_user(cls, auth_user):
        cls.user_id = auth_user.get('id')
        cls.username = auth_user.get('username')
        cls.status = auth_user.get('status')
        cls.roles = auth_user.get('roles')
        cls.permissions = auth_user.get('permissions')
        return cls()

    def __iter__(self):
        """
        可迭代
        :return:
        """
        return (key for key in dir(self) if not key.startswith('__'))

    def to_dict(self):
        """
        类属性转dict
        :return:
        """
        result_dict = {
            key: getattr(self, key)
            for key in self
            if type(getattr(self, key)) is not types.MethodType
        }
        return result_dict


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
