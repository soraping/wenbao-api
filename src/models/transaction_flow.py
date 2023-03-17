#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 14:55
# @Name    : transaction_flow.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 交易流水

from peewee import (
    IntegerField
)
from .base import BaseModel


class TransactionFlowModel(BaseModel):
    """
    交易流水
    """
    user_id = IntegerField(verbose_name='user', help_text='用户流水')


    class Meta:
        table_name = 'transaction_flow'
