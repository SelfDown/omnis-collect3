# -*- coding: utf-8 -*-
"""
@Time: 2021/7/28 13:43
@Author: zzhang zzhang@cenboomh.com
@File: console.py
@desc:
"""
from django.shortcuts import render


def console(request):
    return render(request, 'console/index.html')
