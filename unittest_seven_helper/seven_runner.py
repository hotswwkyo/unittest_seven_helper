#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author: 思文伟
@Date: 2021/09/17
'''
from unittest.runner import TextTestRunner
from .seven_result import SevenTestResult


class SevenTestRunner(TextTestRunner):

    resultclass = SevenTestResult
