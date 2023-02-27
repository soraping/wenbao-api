from src.models import UserModel
from src.config.context import Request
from src.utils import exceptions, gen_password


async def query_user_by_id(request: Request, user_id: str) -> UserModel:
    user_data_gen = await request.ctx.db.execute(
        UserModel.select().where((UserModel.id == user_id))
    )
    return user_data_gen[0]


async def query_user_by_login(request: Request, data) -> UserModel:
    user_data_gen = await request.ctx.db.execute(
        UserModel.select().where((UserModel.username == data['username']))
    )
    if len(list(user_data_gen)) > 0:
        user: UserModel = user_data_gen[0]
        verify_password = gen_password(data['password'], user.salt)
        if verify_password != user.password:
            raise exceptions.UserClientError(message="用户名或密码错误")
        else:
            return user
    else:
        raise exceptions.UserClientError(message="用户名或密码错误")
