#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/28 15:28
# @Name    : manage.py
# @email   : 541251250@qq.com
# @Author  : caoping

import click
import inquirer
import asyncio
import peewee
import typing
from rich.console import Console
from rich import print as rprint
from src.config import CONFIG
from src.extension import InitMysql
from migrations import MigratorOperate
from src.models import (
    PermissionModel,
    RolePermissionModel,
    RoleTypeEnum,
    RoleModel,
    UserModel,
    UserRoleModel
)
from src.utils import gen_random, gen_password, auto_load_gen

config_data = CONFIG.get_config()
mgr = InitMysql(config_data['mysql']).mgr()

console = Console()


def log(msg, mode='info'):
    style = {
        'info': "bold blue",
        'warn': "bold yellow",
        'error': "bold red",
        'start': 'bold yellow',
        'done': "bold green"
    }
    console.print(f'【{config_data["PROJECT_NAME"]}】{msg}', style=style[mode])


async def run():
    log("开始安装...", mode='start')
    await create_table()
    await permissions()
    await role()
    admin_user_id = await admin()
    log(f"管理员账号 => {admin_user_id}")
    await relation(admin_user_id)
    await mgr.close()
    log("安装完成", mode='done')


async def create_table():
    log("开始创建数据表...")
    # 获取模块
    models = auto_load_gen('src.models.__init__')
    for model in models:
        # 通过子类判断更加合理
        if type(model) != typing._GenericAlias and issubclass(model, peewee.Model):
            MigratorOperate(model)
            log(f"生成表 {model._meta.table_name}")

    log("数据表创建完成!", mode='done')


async def permissions():
    log("初始化权限表...")
    permissions = [
        {
            'label': '主控台',
            'value': 'dashboard_console',
        },
        {
            'label': '监控页',
            'value': 'dashboard_monitor',
        },
        {
            'label': '工作台',
            'value': 'dashboard_workplace',
        },
        {
            'label': '基础列表',
            'value': 'basic_list',
        },
        {
            'label': '基础列表删除',
            'value': 'basic_list_delete',
        },
    ]

    await mgr.execute(
        PermissionModel.insert_many(permissions)
    )
    log("系统默认权限设置完成!", mode='done')


async def role():
    log("初始化系统默认角色...")
    role_list = [
        {
            "name": "管理员",
            "type": RoleTypeEnum.ADMIN.value
        },
        {
            "name": "员工",
            "type": RoleTypeEnum.EMPLOYEE.value
        },
        {
            "name": "用户",
            "type": RoleTypeEnum.USER.value
        }
    ]
    await mgr.execute(
        RoleModel.insert_many(role_list)
    )
    log("系统默认角色创建完成!", mode='done')


async def admin():
    log("初始化管理员账号...")
    admin_data = config_data.get('ADMIN', dict(username="admin", password="admin123"))
    salt = gen_random(length=12)
    admin_data['salt'] = salt
    admin_data['password'] = gen_password(admin_data['password'], salt)
    admin_data['age'] = 10
    rprint(admin_data)
    user_id = await mgr.execute(
        UserModel.insert(**admin_data)
    )
    log("管理员账号创建完成！", mode='done')
    return user_id


async def relation(admin_user_id):
    log("初始角色权限关系表...")
    # 角色
    role_models = await mgr.execute(
        RoleModel.select(RoleModel.type, RoleModel.id).where((RoleModel.type == RoleTypeEnum.ADMIN.value) | (RoleModel.type == RoleTypeEnum.EMPLOYEE.value))
    )
    roles = list(role_models)
    # 管理员账号信息
    admin_role = [role for role in roles if role.model_to_dict()['type'] == RoleTypeEnum.ADMIN.value][0]
    # 权限
    permission_models = await mgr.execute(
        PermissionModel.select(PermissionModel.id, PermissionModel.value)
    )
    permissions = list(permission_models)

    # 角色权限分配
    permission_list = [
        {
            "role": role.id,
            "permission": permission.id
        }
        for role in roles
        for permission in permissions
    ]

    await mgr.execute(
        RolePermissionModel.insert_many(permission_list)
    )

    log("角色权限关系表初始化完成！", mode='done')

    log("初始会员角色关系表...")
    # 管理员的会员信息
    await mgr.execute(
        UserRoleModel.insert(user=admin_user_id, role=admin_role.id)
    )
    log("会员角色关系表初始化完成！", mode='done')


if __name__ == '__main__':
    asyncio.run(run())
