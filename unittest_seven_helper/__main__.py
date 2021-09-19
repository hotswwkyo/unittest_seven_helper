#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Main entry point
code from unittest.__main__.py
'''

import sys
if sys.argv[0].endswith("__main__.py"):
    import os.path
    # We change sys.argv[0] to make help message more useful
    # use executable without path, unquoted
    # (it's just a hint anyway)
    # (if you have spaces in your executable you get what you deserve!)
    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + " -m unittest_seven_helper"
    del os

__unittest = True

from .main import main

main(module=None)
