#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    EweeStats
    ~~~~~~~~~
    
    :copyright: Copyright 2014 Gabriel Hondet <gabrielhondet@gmail.com>
    :license: Apache 2.0, see LICENSE for details
"""

import imp
import sys

__version__ = '0.0dev2'

def main(argv=sys.argv):
    """Return a boolean indicating if the module is available"""
    try:
        imp.find_module('ezodf2')
        odsWrite = True
    except ImportError:
        odsWrite = False

    """Check python version"""
    if sys.version_info[:3] < (2, 7, 0):
        sys.stderr.write('Error: EweeStats requires at least Python 2.7 to run.\n')
        return 1

    print('Init done')
    print(argv)

main()
