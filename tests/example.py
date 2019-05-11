#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ??
@file: example.py
@time: 2019/4/26 15:33
@desc:
'''


def func(x):
    return x + 1


"""
pytest会在该目录中寻找以test开头的文件
进入测试文件中寻找以test_开头的函数并执行
测试函数以断言assert结尾
"""


def test_answer():
    assert func(3) == 4
