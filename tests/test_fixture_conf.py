#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ??
@file: test_fixture_conf.py
@time: 2019/4/28 9:43
@desc:
'''


def test_3(before):
    print('test_3()')


def test_4(before):
    print('test_4()')
    for item in before.items():
        print(item)
