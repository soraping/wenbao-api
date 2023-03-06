#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 15:16
# @Name    : forms.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 表单
from typing import Callable, Dict
from sanic_wtf import SanicForm as _SanicForm
from wtforms import (
    BooleanField, PasswordField, SelectField,
    SelectMultipleField, StringField, SubmitField, TextAreaField, IntegerField
)
from wtforms.validators import DataRequired
from wtforms.form import Form
import wtforms_json

# 表单提交校验支持json
wtforms_json.init()


class SanicForm(_SanicForm):
    # 新增这个类属性
    # 1. 为了idea能识别提示 2. 可以多一个引用
    @classmethod
    def from_json(cls, formdata: Dict = None) -> _SanicForm:
        # 子类调用父类的classmethod,一定要用super来改变cls的指向，不要直接调用
        return super(SanicForm, cls).from_json(formdata=formdata)


class UserForm(SanicForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class MenuForm(SanicForm):
    name = StringField('name', validators=[DataRequired()])
    icon = StringField('icon')
    type = StringField('type')
    path = StringField('path', validators=[DataRequired()])
    component = StringField('component')
    redirect = StringField('redirect')
    permission = StringField('permission')
    parent = IntegerField('parent')


if __name__ == '__main__':
    ...
