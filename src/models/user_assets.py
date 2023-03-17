#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 14:18
# @Name    : user_assets.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 会员资产

from peewee import (
    IntegerField,
    DecimalField
)
from .base import BaseModel


class UserAssetsModel(BaseModel):
    """
    会员资金
    """
    user_id = IntegerField(verbose_name='user id', help_text='会员编号')
    integral = DecimalField(verbose_name='user integral', help_text='会员积分', default=0)
    balance = DecimalField(verbose_name='user balance', help_text='会员余额', default=0)
    locking = DecimalField(verbose_name='user locking balance', help_text='会员锁定余额', default=0)

    class Meta:
        table_name = 'user_assets'
