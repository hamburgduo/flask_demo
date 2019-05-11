#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ??
@file: conftest.py.py
@time: 2019/4/28 9:42
@desc:
'''
"""
conftest.py中的fixture函数，可以在多个文件中直接引用
实现fixture函数的复用
"""

import pytest


@pytest.fixture()
def before():
    print('\nbefore each test')
    return {"data": 1, "msg": "testing..."}
