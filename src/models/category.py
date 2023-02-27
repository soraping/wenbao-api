#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/5 13:12
# @Name    : category.py
# @email   : 541251250@qq.com
# @Author  : caoping

from peewee import (
    PrimaryKeyField,
    CharField,
    IntegerField
)
from .base import BaseModel


class CategoryModel(BaseModel):
    """
    分类
    """
    id = PrimaryKeyField()
    parentId = IntegerField(verbose_name='parentId', null=True)
    name = CharField(max_length=20, verbose_name='cate name')
    logo = CharField(max_length=50, verbose_name='cate logo url', null=True)
    status = IntegerField(verbose_name='cate status')
    sort = IntegerField(verbose_name='cate sort')

    class Meta:
        table_name = 'category'