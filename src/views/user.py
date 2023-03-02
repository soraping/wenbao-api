from sanic import Blueprint
from src.extension.jwt_ext import JwtExt
from src.services import users_service
from src.utils import request_log, ResponseBody
from src.config.context import Request
from src.forms import UserForm

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
    user_login_form = UserForm.from_json(request.json)
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


@admin_user_bp.get('/menu/list')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_menu_list(request: Request):
    """
    获取所有菜单列表
    :param request:
    :return:
    """
    return await users_service.query_menu_list(request)


@admin_user_bp.post('/menu/add')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_menu_add(request: Request):
    """
    新增菜单
    :param request:
    :return:
    """
    body = request.json
    await users_service.add_menu(request, body)
