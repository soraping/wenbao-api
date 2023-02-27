from dataclasses import dataclass
from peewee_async import Manager
from sanic import Request as SanicRequest


@dataclass
class AuthUser:
    role: str
    user_id: str


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