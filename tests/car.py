#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: ??
@file: car.py
@time: 2019/4/26 15:42
@desc:
'''


from data.car import Car


def test_car_brake():
    car = Car(50)
    car.brake()
    assert car.speed == 45