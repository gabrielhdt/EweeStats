#!/usr/bin/env python2
# -*-coding: utf-8 -*-
#  setup.py
# Author: Gabriel Hondet
# Purpose: setup
#
#  Copyright 2014 Gabriel Hondet <gabrielhondet@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#


try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    long_description = f.read()
with open('CHANGES') as c:
    changes = c.read()

setup(
    name='EweeStats',
    version='0.1',
    platforms='POSIX',
    packages=find_packages(),
    package_data = {
        # Includes all *.txt and *.md
        '': ['*.txt', '*.md', '*.rst'],
    },
    include_package_data = True,
    install_requires=['pyFirmata', 'pygal', 'pyserial', 'lxml', 'ezodf2', 'subprocess32'],
    scripts=['eweestats', 'EweeStats/create_files.sh'],
    data_files=[('/etc/eweestats', ['cfg/eweestats.conf']),
                ('/etc/init.d', ['startscript/eweestats.sh']),
                ('/usr/sbin', ['eweestats'])],
    
    # Metada for upload to PyPi
    description='Program to read, process, present and broadcast datas from sensors',
    author='Gabriel Hondet',
    author_email="gabrielhondet@gmail.com",
    license='GPL 3',
    url='https://github.com/gabrielhdt/github',
    long_description=long_description + changes,
    )
