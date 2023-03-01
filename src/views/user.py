from sanic import Blueprint
from src.extension.jwt_ext import JwtExt
from src.services import users_service
from src.utils import request_log, ResponseBody
from src.config.context import Request

admin_user_bp = Blueprint('admin-user', url_prefix='/admin/user')
user_bp = Blueprint('user', url_prefix='/user')


@user_bp.post('/login')
@ResponseBody()
async def user_login(request: Request):
    """
    登录
    :param request:
    :return:
    """
    body = request.json
    user_data = await users_service.query_user_by_login(request, body)
    token = JwtExt.create_access_token(user_data['id'], {'user_id': user_data['id']})
    user_data['token'] = token
    return user_data


@admin_user_bp.get('/info')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_user_data(request: Request):
    """
    管理员账号信息
    :param request:
    :return:
    """
    return request.ctx.auth_user


@admin_user_bp.get('/role/list')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_role_list(request: Request):
    """
    角色列表
    :param request:
    :return:
    """
    return await users_service.query_user_role_list(request)

# @user_bp.get('/detail')
# @openapi.summary('user detail')
# @JwtExt.login_required()
# async def user_data(request: Request):
#     login_data = request.ctx.auth_user
#     return {"data": login_data}


# @user_bp.get('/info/<user_id>')
# @openapi.summary('user info')
# @JwtExt.login_required()
# @JwtExt.scopes([RoleTypeEnum.ADMIN.value])
# @request_log
# async def user_data(request: Request, user_id: str):
#     login_data = request.ctx.auth_user
#     return login_data


# @user_bp.post('/register')
# @openapi.summary('user register')
# async def user_register(request: Request):
#     body = request.json
#     token = JwtExt.gen_token("c123123", body)
#     result = dict(**body, **dict(token=token))
#     return response.json({"data": result})


# @user_bp.get('/list')
# @openapi.summary('user list')
# async def get_user_list(request):
#     return {"msg": "hello world"}
