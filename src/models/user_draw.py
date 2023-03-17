#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 15:00
# @Name    : user_draw.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 用户提现申请列表

from peewee import (
    IntegerField,
    CharField,
    DateTimeField,
    DecimalField
)
import datetime
from .base import BaseModel


class UserDraw(BaseModel):
    """
    用户提现
    """
    user_id = IntegerField(verbose_name='user id')
    draw = DecimalField(verbose_name='draw money', help_text='提现金额')
    way = IntegerField(choices=((0, '支付宝'), (1, '微信'), (2, '银行卡')), verbose_name='user draw way', default=0, help_text='提现方式')
    status = IntegerField(choices=((0, '待审核'), (1, '审核通过'), (2, '审核失败')), verbose_name='user draw apply', default=0)
    audit_time = DateTimeField(null=True, default=datetime.datetime.utcnow, formats='%Y-%m-%d %H:%M:%S', verbose_name='audit time')
    audit_remark = CharField(null=True, max_length=50, verbose_name='audit remark', help_text='审核备注')
    audit_user_id = CharField(null=True, verbose_name='audit user id', help_text='审核员')
    audit_ip = CharField(null=True, max_length=20, verbose_name='audit ip', help_text='审核人IP')


    class Meta:
        table_name = 'user_draw'