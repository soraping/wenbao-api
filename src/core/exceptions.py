from sanic import Sanic, exceptions, Request
from sanic.handlers import ErrorHandler
from sanic.log import logger
from sanic.response import json
from src.constant import ResponseTypeEnum
import pymysql


class ConfigurationConflictError(exceptions.SanicException):
    """
    配置异常
    """
    ...


class JWTTokenDecodeError(exceptions.SanicException):
    status_code = 400
    message = "jwt-token 过期或解析失败"


class InvalidJWTTokenError(exceptions.SanicException):
    """
    jwt 解析失败
    """
    status_code = 422
    message = "Authorization invalid"


class NoAuthorizationError(exceptions.SanicException):
    """
    token 不存在
    """
    status_code = 401
    message = "header must has authorization"


class RoleScopesRequestError(exceptions.SanicException):
    """
    角色权限
    """
    status_code = 400
    message = "user role can not request"


class UserHasNoPermissionRequest(exceptions.SanicException):
    """
    权限不够
    """
    status_code = 400
    message = "user has not permission to request"


class MysqlConnectionError(exceptions.SanicException):
    """
    数据库连接失败
    """
    status_code = 500
    message = "mysql connection error"


class UserClientError(exceptions.SanicException):
    """
    客户端请求错误
    """
    status_code = 400


class ModelDoesNotExist(exceptions.SanicException):
    """
    查无此人
    """
    status_code = 400


class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        return super().default(request, exception)
        # return json({'message': str(exception), 'code': self.code, "type": ResponseTypeEnum.ERROR.value})


class InitErrorHandler:

    def __init__(self, code):
        self.code = code

    @classmethod
    def initialize(cls, app: Sanic):
        app.error_handler.add(exceptions.ServerError, cls._handler(exceptions.ServerError.status_code))
        app.error_handler.add(exceptions.NotFound, cls._handler(exceptions.NotFound.status_code))
        app.error_handler.add(JWTTokenDecodeError, cls._handler(10042))
        app.error_handler.add(pymysql.err.OperationalError, cls._handler(-1))
        # app.error_handler = CustomErrorHandler()

    @classmethod
    def _handler(cls, code):
        return cls(code)

    def __call__(self, request: Request, error: exceptions.SanicException):
        logger.error(str(error))
        return json({'message': str(error), 'code': self.code, "type": ResponseTypeEnum.ERROR.value})
