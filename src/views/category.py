#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 19:19
# @Name    : category.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 分类

from sanic import Blueprint
from src.core.context import Request
from src.services import category as category_service
from src.forms import CategoryForm
from src.utils import request_log, ResponseBody
from src.extension.jwt_ext import JwtExt

admin_category_bp = Blueprint('admin-category', url_prefix='/admin/goods/category')
goods_category_bp = Blueprint('category', url_prefix='/goods/category')


@admin_category_bp.post('/list')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_category_list(request: Request):
    """
    分类列表
    :param request:
    :return:
    """
    return await category_service.category_list(request)


@admin_category_bp.post('/add')
@JwtExt.login_required()
@request_log
@ResponseBody()
async def admin_category_add(request: Request):
    """
    新增分类
    :param request:
    :return:
    """
    category_form = CategoryForm.from_json(request.json)
    await category_service.category_add(request, category_form.data)