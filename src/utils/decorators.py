from functools import wraps


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