from typing import Dict, AnyStr
import orjson
from functools import wraps, singledispatch
from sanic import HTTPResponse
from sanic.log import logger
from src.config.context import Request


@singledispatch
def json_prettify(data):
    """
    json 美化输出
    orjson.dumps 返回bytes ，不是str，需要decode
    :param data:
    :return:
    """
    return repr(data)


@json_prettify.register(dict)
def _(data):
    return orjson.dumps(data, option=orjson.OPT_INDENT_2).decode('utf-8')


@json_prettify.register(bytes)
def _(data):
    res = orjson.loads(data)
    return orjson.dumps(res, option=orjson.OPT_INDENT_2).decode('utf-8')


def request_log(func):
    @wraps(func)
    async def decorator(request: Request, *args, **kwargs):
        # 请求日志打印
        request_id = str(request.id)
        logger.info(f"request_id={request_id}\trequest_url={request.uri_template}")
        login_user = request.ctx.auth_user
        log_data = {
            'request_id': request_id,
            'method': request.method,
            'uri': request.uri_template,
            'user-agent': request.headers.get('user-agent', ''),
            'clientType': request.headers.get('clientType', ''),
            'query': request.query_string,
            'path': request.match_info
        }

        if request.method == 'POST':
            log_data['data'] = request.json

        if login_user:
            log_data['login_user'] = login_user.to_dict()

        # json.dumps(request_data, indent=4) 美化输出
        logger.info(f"\nrequest_id={request_id}\nrequest_log={json_prettify(log_data)}")
        func_data = await func(request, *args, **kwargs)
        # 做个返回值保护
        result_data = func_data.body if isinstance(func_data, HTTPResponse) else func_data
        logger.info(f"\nrequest_id={request_id}\nresponse_log={json_prettify(result_data)}")
        return func_data

    return decorator
