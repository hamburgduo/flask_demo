#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ??
@file: test_class_a.py
@time: 2019/4/28 15:33
@desc:
'''
"""
1.测试类所在的文件以test_开头
2.测试类以Test开头，并且不能带有__init__方法
3.类中测试函数以test_开头
4.测试函数以assert断言结尾
"""

class TestClassA:
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')