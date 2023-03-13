#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/13 14:26
# @Name    : base.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    :
import types


class BaseBean:

    def __iter__(self):
        """
        可迭代
        :return:
        """
        return (key for key in dir(self) if not key.startswith('__'))

    def to_dict(self):
        """
        类属性转dict
        :return:
        """
        result_dict = {
            key: getattr(self, key)
            for key in self
            if type(getattr(self, key)) is not types.MethodType
        }
        return result_dict
