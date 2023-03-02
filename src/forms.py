#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 15:16
# @Name    : forms.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 表单
from sanic_wtf import SanicForm as _SanicForm
from wtforms import (
    BooleanField, PasswordField, SelectField,
    SelectMultipleField, StringField, SubmitField, TextAreaField
)
from wtforms.validators import DataRequired
import wtforms_json

# 表单提交校验支持json
wtforms_json.init()


class SanicForm(_SanicForm):
    ...
    # @classmethod
    # def from_json(cls, data_json):
    #     return cls


class UserForm(SanicForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
