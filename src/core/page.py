#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/12 19:05
# @Name    : page.py
# @email   : 541251250@qq.com
# @Author  : caoping
# @desc    : 分页
from typing import List


class Page:
    dataList: List
    pageNo: int
    pageSize: int
    pageTotal: int


class PageListResponse:

    def __init__(self, dataList: List = [], pageNo: int = 0, pageSize: int = 10, pageTotal: int = 0):
        self.dataList = dataList
        self.pageNo = pageNo
        self.pageSize = pageSize
        self.pageTotal = pageTotal

    @classmethod
    def to_dict(cls, data: Page):
        return cls(
            dataList=data.dataList,
            pageNo=data.pageNo,
            pageSize=data.pageSize,
            pageTotal=data.pageTotal
        )