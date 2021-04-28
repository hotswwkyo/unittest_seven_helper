#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author: 思文伟
@Date: 2021/03/30 11:21:57
'''
import time
import inspect
import unittest
from unittest.util import strclass
from .test_wrapper import Test


class AbstractTestCase(unittest.TestCase):
    """为测试类添加自动收集和自行测试用例的方法"""
    def __init__(self, methodName='runTest', serial_number=1):
        super(AbstractTestCase, self).__init__(methodName)
        self._serial_number = serial_number

    @classmethod
    def sleep(cls, seconds):

        time.sleep(seconds)
        return cls

    @property
    def test_method_obj(self):
        return getattr(self, self._testMethodName)

    @property
    def _test_method_name(self):

        return "{}_{}".format(self._testMethodName, self._serial_number)

    def id(self):
        return "{}.{}".format(strclass(self.__class__), self._test_method_name)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        return self._test_method_name == other._test_method_name

    def __hash__(self):
        return hash((type(self), self._test_method_name))

    def __str__(self):
        return "%s (%s)" % (self._test_method_name, strclass(self.__class__))

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (strclass(self.__class__), self._test_method_name)

    @classmethod
    def collect_testcases(cls):

        members = [obj_val for obj_key, obj_val in cls.__dict__.items() if inspect.ismethod(obj_val) or inspect.isfunction(obj_val)]
        test_func_list = [member for member in members if Test.func_has_test_marker(member)]
        run_test_func_list = [tf for tf in test_func_list if Test.get_test_marker(tf, key=Test.ENABLED, default_value=False)]
        run_test_func_list.sort(key=lambda tf: Test.get_test_marker(tf, key=Test.PRIORITY, default_value=1))
        testcases = []
        for test_func in run_test_func_list:
            test_func.collect_test_datasets(cls, test_func)
            datasets = test_func.test_settings[Test.TEST_DATASETS]
            if (len(datasets) > 0):
                for i, v in enumerate(datasets):
                    testcases.append(cls(test_func.__name__, (i + 1)))
            else:
                testcases.append(cls(test_func.__name__))
        return testcases

    @classmethod
    def build_self_suite(cls):

        suite = unittest.TestSuite()
        suite.addTests(cls.collect_testcases())
        return suite

    @classmethod
    def run_test(cls):

        runner = unittest.TextTestRunner()
        return runner.run(cls.build_self_suite())
