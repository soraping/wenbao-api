#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/15 10:42
# @Name    : cache.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    :

from functools import wraps
from src.core.context import Request


def async_cache(maxsize=128):
    """
    协程的简易缓存
    依赖redis/内存
    :param maxsize:
    :return:
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            ...

    return decorator
