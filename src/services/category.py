#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 19:19
# @Name    : category.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 分类

from typing import List
from src.core.context import Request
from src.models import GoodsCategoryModel
from src.core import exceptions


async def category_add(request: Request, data):
    """
    新增分类
    :param request:
    :param data:
    :return:
    """
    # 校验分类数据
    if data['parent']:
        cate_parent = await request.ctx.db.scalar(
            GoodsCategoryModel.select().where(GoodsCategoryModel.id == data['parent']),
            as_tuple=False
        )
        if cate_parent is None:
            raise exceptions.UserClientError(f"父级分类{data['parent']}已经被删除")

    # 总数
    cate_count = await request.ctx.db.count(
        GoodsCategoryModel.select()
    )

    if cate_count > 100:
        raise exceptions.UserClientError(f"分类数目超过最大数")

    await request.ctx.db.execute(
        GoodsCategoryModel.insert(**data)
    )


async def category_upd(request: Request, data):
    """
    修改分类
    :param request:
    :param data:
    :return:
    """
    if data['id'] is None:
        raise exceptions.UserClientError(f"请选择分类")

    await request.ctx.db.execute(
        GoodsCategoryModel.update(**data).where(GoodsCategoryModel.id == data['id'])
    )


async def category_del(request: Request, cate_id):
    """
    分类删除
    :param request:
    :param cate_id:
    :return:
    """
    # 是否有子分类
    child_cate = await request.ctx.db.scalar(
        GoodsCategoryModel.select().where(GoodsCategoryModel.parent == cate_id)
    )
    if child_cate:
        raise exceptions.UserClientError(f"该分类存在子类，不能删除")

    await request.ctx.db.execute(
        GoodsCategoryModel.delete().where(GoodsCategoryModel.id == cate_id)
    )


async def category_list(request: Request):
    category_model_list: List[GoodsCategoryModel] = await request.ctx.db.execute(
        GoodsCategoryModel.select().where(
            GoodsCategoryModel.status == 1
        )
    )

    return [
        category.model_to_dict(exclude=[
            GoodsCategoryModel.update_time,
            GoodsCategoryModel.status,
            GoodsCategoryModel.create_time
        ])
        for category in category_model_list
    ]