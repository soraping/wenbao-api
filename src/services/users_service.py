from typing import List
from peewee import DoesNotExist, JOIN
from src.models import (
    UserModel,
    RoleModel,
    UserRoleModel,
    RolePermissionModel,
    MenuModel
)
from src.config.context import Request
from src.utils import exceptions, gen_password


async def query_user_by_login(request: Request, data):
    """
    登录信息查询
    :param request:
    :param data:
    :return:
    """
    try:
        user_data = await request.ctx.db.get(
            UserModel.select().where((UserModel.username == data['username']))
        )
        verify_password = gen_password(data['password'], user_data.salt)
        if verify_password != user_data.password:
            raise exceptions.UserClientError
        else:
            user_result_dict = user_data.model_to_dict(exclude=[UserModel.password, UserModel.salt])
            # 查询角色
            roles, permissions = await query_user_roles_and_permissions(request, user_result_dict.get('id'))
            user_result_dict['roles'] = roles
            # 获取权限
            user_result_dict['permissions'] = permissions
            return user_result_dict
    except (DoesNotExist, exceptions.UserClientError) as e:
        raise exceptions.UserClientError(message="用户名或密码错误")


async def query_user_by_id(request: Request, user_id: str):
    """
    根据Id查询用户信息
    :param request:
    :param user_id:
    :return:
    """
    try:
        user_data = await request.ctx.db.get(
            UserModel.select(
                UserModel.username,
                UserModel.id,
                UserModel.age
            ).where((UserModel.id == user_id))
        )

        auth_user_result_dict = user_data.model_to_dict()
        roles, permissions = await query_user_roles_and_permissions(request, auth_user_result_dict.get('id'))
        auth_user_result_dict['roles'] = roles
        # 获取权限
        auth_user_result_dict['permissions'] = permissions

        return auth_user_result_dict

    except (DoesNotExist, exceptions.UserClientError) as e:
        raise exceptions.UserClientError(message="用户名或密码错误")


async def query_user_roles_and_permissions(request: Request, user_id):
    """
    获取用户的角色及权限
    :param request:
    :param user_id:
    :return:
    """
    # 查询角色
    roles = await query_user_roles_by_user_id(request, user_id)
    # 获取权限
    role_ids = [role['role_id'] for role in roles]
    permissions = await query_user_permissions_by_role(request, role_ids)
    return (roles, permissions)


async def query_user_roles_by_user_id(request: Request, user_id):
    """
    查询该用户的角色
    :param request:
    :param user_id:
    :return:
    """
    # fields = [
    #     UserRoleModel.user.alias("user_id"),
    #     RoleModel.id.alias("role_id"),
    #     RoleModel.name.alias("role_name"),
    #     RoleModel.type.alias("role_type")
    # ]

    user_roles: List[UserRoleModel] = await request.ctx.db.execute(
        UserRoleModel.select(UserRoleModel.user, RoleModel)
            .join(RoleModel, JOIN.LEFT_OUTER, on=(UserRoleModel.role == RoleModel.id))
            .where(UserRoleModel.user == user_id)
    )

    return [
        {
            'role_id': user_role.role.id,
            'role_type': user_role.role.type,
            'role_name': user_role.role.name
        }
        for user_role in user_roles
        if user_role.role is not None
    ]


async def query_user_permissions_by_role(request: Request, role_ids):
    """
    查询角色权限
    合并权限集合
    :param request:
    :param role_ids:
    :return:
    使用这样的写法去重
    .select(RolePermissionModel.permission).distinct()
    select 语句中添加需要去重的字段依据
    """
    role_permissions: List[RolePermissionModel] = await request.ctx.db.execute(
        RolePermissionModel.select(RolePermissionModel.permission).distinct().where(
            RolePermissionModel.role.in_(role_ids))
    )

    return [
        {
            "label": permission.permission.label,
            "value": permission.permission.value
        }
        for permission in role_permissions
        if permission.permission is not None
    ]


async def add_menu(request: Request, data):
    """
    新增菜单
    :param request:
    :param data:
    :return:
    """
    await request.ctx.db.execute(
        MenuModel.insert(**data)
    )


async def query_all_menu_list(request: Request):
    """
    获取菜单所有列表
    :param request:
    :return:
    """
    menu_list: List[MenuModel] = await request.ctx.db.execute(
        MenuModel.select().where(MenuModel.status == 1)
    )

    return [
        menu_model.model_to_dict(exclude=[MenuModel.create_time, MenuModel.update_time])
        for menu_model in menu_list
    ]


async def query_user_menu_list(request: Request):
    """
    查询该用户权限下列表
    :param request:
    :return:
    """
    auth_user = request.ctx.auth_user
    user_permissions = [permission['value'] for permission in auth_user['permissions']]
    all_menu_list = await query_all_menu_list(request)
    # 根据权限筛选菜单
    return [menu for menu in all_menu_list if menu.get('permission') in user_permissions]



async def query_user_role_list(request: Request):
    """
    查询角色列表
    :param request:
    :return:
    """
    ...
