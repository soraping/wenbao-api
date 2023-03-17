#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 18:58
# @Name    : goods_category.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 商品分类

from peewee import (
    CharField,
    IntegerField
)
from .base import BaseModel


class GoodsCategoryModel(BaseModel):
    """
    商品分类
    """
    name = CharField(max_length=20, unique=True, verbose_name='cate name', help_text='分类名称')
    parent = IntegerField(null=True, verbose_name='parent category', help_text='父级分类')
    allow_level = IntegerField(null=True, verbose_name='allow user view', help_text='允许访问的星级')
    logo_url = CharField(null=True, max_length=50, verbose_name='category logo', help_text='分类图片')
    sort = IntegerField(verbose_name='category sort', default=0)
    online_time = CharField(null=True, max_length=50, verbose_name='open time', help_text='开放时间段')
    status = IntegerField(choices=((0, '已删除'), (1, '正常'), (2, '隐藏')), verbose_name='cate status', default=1)

    class Meta:
        table_name = 'goods_category'
