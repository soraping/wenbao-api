import random
import hashlib
import importlib
from typing import AnyStr, Generator
from . import exceptions as custom_exceptions
from .decorators import singleton
from .log import request_log


def auto_load_gen(path: str) -> Generator:
    """
    根据路径，自动载入模块
    :param path:
    :return:
    """
    modules = importlib.import_module(str(path))
    # 过滤掉模块内的魔术方法，返回模块真实对象
    return (getattr(modules, args) for args in modules.__dict__ if not args.startswith('__'))


def gen_random(mode='mixDigitLetter', length=16):
    """
    按照不同模式生成随机字符串
    :return:
    """
    upper_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_letter = "abcdefghigklmnopqrstuvwxyz"
    digits = "0123456789"
    wpecial_characters = "!@#$%&_-.+="
    random_map = {
        "digit": digits,
        "upper": upper_letter,
        "lower": lower_letter,
        "mixDigitLetter": upper_letter + lower_letter + digits,
        "mixLetter": upper_letter + lower_letter,
        "mixDigitLetterCharcter": upper_letter + lower_letter + digits + wpecial_characters
    }

    str_list = [random.choice(random_map[mode]) for i in range(length)]
    random_str = ''.join(str_list)
    return random_str


def md5(content):
    """
    md5 加密
    :param content:
    :return:
    """
    m = hashlib.md5(content.encode(encoding='utf-8'))
    return m.hexdigest()


def gen_password(password: AnyStr, salt: AnyStr):
    """
    密码生成器
    salt 嵌在 password 中
    :param password:
    :param salt:
    :return:
    """
    return md5(salt.join(password))



__all__ = [
    'singleton',
    'gen_random',
    'md5',
    'gen_password',
    'auto_load_gen',
    'custom_exceptions',
    'request_log'
]