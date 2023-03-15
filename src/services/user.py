from typing import List
from peewee import DoesNotExist, JOIN
from sanic.log import logger
from src.models import (
    UserModel,
    RoleModel,
    UserRoleModel,
    RolePermissionModel,
    PermissionModel
)
from src.core.context import Request
from src.utils import gen_password
from src.core import exceptions
from src.core.page import PageListResponse


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
                UserModel.age,
                UserModel.status
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
            "id": permission.permission.id,
            "label": permission.permission.label,
            "key": permission.permission.key,
            "value": permission.permission.value
        }
        for permission in role_permissions
        if permission.permission is not None
    ]


async def query_user_role_list(request: Request):
    """
    查询角色列表
    :param request:
    :return:
    """
    # 获取列表查询参数
    pageNo = 1
    pageSize = 10

    # 总数
    pageTotal = await request.ctx.db.count(
        RoleModel.select(RoleModel.name)
            .where(RoleModel.status == 1)
    )

    role_models: List[RoleModel] = await request.ctx.db.execute(
        RoleModel
            .select()
            .where(RoleModel.status == 1)
            .paginate(pageNo, pageSize)
    )
    data_list = [
        role.model_to_dict(exclude=[RoleModel.update_time, RoleModel.status])
        for role in role_models
    ]

    return PageListResponse.result(dataList=data_list, pageNo=pageNo, pageSize=pageSize, pageTotal=pageTotal)


async def add_user_role(request: Request, role):
    """
    新增角色
    :param request:
    :param role:
    :return:
    """
    await request.ctx.db.execute(
        RoleModel.insert(**role)
    )


async def upd_user_role(request: Request, role):
    """
    更新角色
    :param request:
    :param role:
    :return:
    """
    if role['id']:
        raise exceptions.UserClientError("更新角色必须选中一个角色才能操作")
    await request.ctx.db.execute(
        RoleModel.update(**role).where(RoleModel.id == role['id'])
    )


async def query_permission_list(request: Request):
    """
    查询权限列表
    :param request:
    :return:
    """
    permissions_models: List[PermissionModel] = await request.ctx.db.execute(
        PermissionModel.select(PermissionModel.id, PermissionModel.label, PermissionModel.value, PermissionModel.key)
    )

    return [
        permission.model_to_dict(only=[
            PermissionModel.id,
            PermissionModel.label,
            PermissionModel.value,
            PermissionModel.key])
        for permission in permissions_models
    ]


async def role_permission_add(request: Request, role_id):
    ...


async def modify_permission_by_role(request: Request, data):
    """
    修改某个角色的权限
    :param request:
    :param data:
    :return:
    """
    select_permission_ids = set([int(i) for i in data['ids']])

    # 当前修改的角色
    role_id = data['role_id']

    # 查询之前的分配权限
    role_permissions = await query_user_permissions_by_role(request, [role_id])
    old_permission_ids = set([
        permission['id']
        for permission in role_permissions
    ])

    """
    核心逻辑，巧用集合的运算
    """
    # 先求交集
    mixed_set = select_permission_ids & old_permission_ids

    # 需要新增集合
    add_permissions_set = select_permission_ids - mixed_set
    # 需要删除集合
    del_permissions = old_permission_ids - mixed_set

    if len(add_permissions_set) > 0:
        await request.ctx.db.execute(
            RolePermissionModel.insert_many([
                dict(role_id=role_id, permission_id=permission_id)
                for permission_id in add_permissions_set
            ])
        )

    if len(del_permissions) > 0:
        await request.ctx.db.execute(
            RolePermissionModel
                .delete()
                .where(RolePermissionModel.role == role_id and RolePermissionModel.permission.in_(del_permissions))
        )

    logger.info(f"切换角色 {role_id} 的权限为 {str(select_permission_ids)}")
