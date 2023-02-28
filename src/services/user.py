from src.models import UserModel, ModelDictType
from src.config.context import Request
from src.utils import exceptions, gen_password


async def query_user_by_login(request: Request, data) -> ModelDictType:
    """
    登录信息查询
    :param request:
    :param data:
    :return:
    """
    user_data_gen = await request.ctx.db.execute(
        UserModel.select().where((UserModel.username == data['username']))
    )
    if len(list(user_data_gen)) > 0:
        user: UserModel = user_data_gen[0]
        verify_password = gen_password(data['password'], user.salt)
        if verify_password != user.password:
            raise exceptions.UserClientError(message="用户名或密码错误")
        else:
            return user.model_to_dict(exclude=[UserModel.password, UserModel.salt])
    else:
        raise exceptions.UserClientError(message="用户名或密码错误")


async def query_user_by_id(request: Request, user_id: str) -> ModelDictType:
    """
    根据Id查询用户信息
    :param request:
    :param user_id:
    :return:
    """
    user_data_gen = await request.ctx.db.execute(
        UserModel.select(
            UserModel.username,
            UserModel.id,
            UserModel.role,
            UserModel.age
        ).where((UserModel.id == user_id))
    )
    if len(list(user_data_gen)) > 0:
        return user_data_gen[0].model_to_dict()
    else:
        raise exceptions.UserClientError(message="查无此人")


async def query_user_permissions(request: Request):
    ...