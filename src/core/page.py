#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/12 19:05
# @Name    : page.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 分页
from typing import List
from .base import BaseBean


class PageListResponse(BaseBean):

    dataList: List
    pageNo: int
    pageSize: int
    pageTotal: int

    @classmethod
    def result(cls, dataList: List = [], pageNo: int = 0, pageSize: int = 10, pageTotal: int = 0):
        cls.dataList = dataList
        cls.pageTotal = pageTotal
        cls.pageNo = pageNo
        cls.pageSize = pageSize
        return cls().to_dict()

