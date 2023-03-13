#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/11 09:51
# @Name    : menu.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 菜单操作

from typing import List
from peewee import DoesNotExist
from src.models import MenuModel
from src.core.context import Request
from src.core import exceptions


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


async def upd_menu(request: Request, data):
    """
    更新菜单
    :param request:
    :param data:
    :return:
    """
    if data['id'] is None:
        raise exceptions.UserClientError("更新菜单必须选中一个菜单才能操作")
    await request.ctx.db.execute(
        MenuModel.update(**data).where(MenuModel.id == data['id'])
    )


async def del_menu(request: Request, menu_id: str):
    """
    删除菜单
    :param request:
    :param menu_id:
    :return:
    """
    menu = await query_menu_by_id(request, menu_id=menu_id)
    # 1. 是否有权限
    allow_permission = menu.permission
    user_permissions = request.ctx.auth_user.permissions
    if allow_permission and allow_permission not in [permission['value'] for permission in user_permissions]:
        raise exceptions.UserHasNoPermissionRequest(message="没有权限删除菜单")
    # 2. 是否有子菜单，没有则可删除
    child_menu = await request.ctx.db.scalar(
        MenuModel.select(MenuModel.name).where(MenuModel.parent == menu_id)
    )
    if child_menu is not None:
        raise exceptions.UserClientError(f"ID={menu_id}菜单有子菜单，不能删除")

    del_num = await request.ctx.db.execute(
        MenuModel.delete().where(MenuModel.id == menu_id)
    )


async def query_menu_by_id(request: Request, menu_id: str):
    """
    查询菜单详情
    :param request:
    :param menu_id:
    :return:
    """
    try:
        menu: MenuModel = await request.ctx.db.get(
            MenuModel.select().where(MenuModel.id == menu_id)
        )
        return menu
    except DoesNotExist:
        raise exceptions.ModelDoesNotExist(f"ID={menu_id}的菜单不存在")


async def query_child_by_id(request: Request, menu_id: str):
    """
    查询子菜单
    :param request:
    :param menu_id:
    :return:
    """
    menus: List[MenuModel] = await request.ctx.db.execute(
        MenuModel.select().where(MenuModel.parent == menu_id)
    )
    return menus


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
    user_permissions = [permission['value'] for permission in auth_user.permissions]
    all_menu_list = await query_all_menu_list(request)
    # 根据权限筛选菜单
    return [menu for menu in all_menu_list if
            menu.get('permission') in user_permissions or menu.get('permission') is None]
