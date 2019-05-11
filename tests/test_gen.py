#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ??
@file: test_gen.py
@time: 2019/5/7 17:57
@desc:
'''

if __name__ == "__main__":
    gen_exp = (x * x for x in range(10))
    for c in gen_exp:
        print(c, end=" ")

