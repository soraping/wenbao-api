from sanic import Blueprint
from src.extension.jwt_ext import JwtExt
from src.services import (
    user as user_service,
    menu as menu_service
)
from src.utils import request_log, ResponseBody
from src.core.context import Request
from src.forms import UserForm, MenuForm, RoleForm

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
    user_login_form = UserForm.from_json(formdata=request.json)
    body = user_login_form.data
    user_data = await user_service.query_user_by_login(request, body)
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
    return request.ctx.auth_user.to_dict()


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
    return await user_service.query_user_role_list(request)


@admin_user_bp.post('/role/add')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_role_add(request: Request):
    """
    角色列表
    :param request:
    :return:
    """
    role_form = RoleForm.from_json(request.json)
    await user_service.add_user_role(request, role_form.data)


@admin_user_bp.get('/owner/menu/list')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def user_menu_list(request: Request):
    """
    获取用户分配的菜单
    :param request:
    :return:
    """
    return await menu_service.query_user_menu_list(request)


@admin_user_bp.get('/all/menu/list')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_all_menu_list(request: Request):
    """
    获取所有菜单列表
    :param request:
    :return:
    """
    return await menu_service.query_all_menu_list(request)


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
    menu_form = MenuForm.from_json(request.json)
    await menu_service.add_menu(request, menu_form.data)


@admin_user_bp.delete('/menu/del/<menu_id>')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_menu_del(request: Request, menu_id):
    """
    新增菜单
    :param request:
    :return:
    """
    await menu_service.del_menu(request, menu_id)


@admin_user_bp.post('/menu/modify')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_menu_modify(request: Request):
    """
    新增菜单
    :param request:
    :return:
    """
    menu_form = MenuForm.from_json(request.json)
    await menu_service.upd_menu(request, menu_form.data)
