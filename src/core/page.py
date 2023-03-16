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

    # 列表数据
    dataList: List
    # 页码数
    pageNo: int
    # 一页数量
    pageSize: int
    # 总页数
    pageCount: int
    # 总数
    total: int

    @classmethod
    def result(cls, dataList: List = [], pageNo: int = 0, pageSize: int = 10, pageCount: int = 0, total: int = 0):
        cls.dataList = dataList
        cls.pageCount = pageCount
        cls.pageNo = pageNo
        cls.pageSize = pageSize
        cls.total = total
        return cls().to_dict()

