from functools import wraps
from sanic import Request
from sanic.response import json
from .constant import ResponseTypeEnum


def singleton(cls):
    """
    单例
    :param cls:
    :return:
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        cache_key = cls.__name__
        if cache_key not in _instances:
            _instances[cache_key] = cls(*args, **kw)
        return _instances[cache_key]

    return instance


class ResponseBody:
    """
    返回值统一封装
    """
    def __init__(self, code=200):
        self.code = code

    def __call__(self, func):
        @wraps(func)
        async def decorator(request: Request, *args, **kwargs):
            res = await func(request, *args, **kwargs)
            return json({
                "code": self.code,
                "result": res,
                "message": "ok",
                "type": ResponseTypeEnum.SUCCESS.value if self.code == 200 else ResponseTypeEnum.ERROR.value
            })

        return decorator
