#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 15:54
# @Name    : goods.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 商品

from peewee import (
    CharField
)
from .base import BaseModel
from src.utils import gen_spu_id


class GoodsModel(BaseModel):
    """
    商品的spu
    """
    spu_id = CharField(default=gen_spu_id(), max_length=10, verbose_name='spuid', unique=True, primary_key=True)
    name = CharField(max_length=30, verbose_name='sup name', help_text='商品spu名称')

    class Meta:
        table_name = 'goods'
