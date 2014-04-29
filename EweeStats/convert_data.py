#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  convert_data.py
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

def convert(valueList):
    """
    :param valueList: liste des valeurs relevées
    :type valueList: list

    :returns: converted datas
    :rtype: list
    """

    # Config : relie à chaque pin un appareil
    sensorList = ['pot', 'pot']
    valueReal = []
    for i in valueList:
        valueReal.append(0.0)

    for i, elt in enumerate(sensorList):
        if elt == 'pot':
            convert_pot(i, valueList, valueReal)

    return valueReal

def convert_pot(pinToPot, valueList, valueReal):
    valueReal[pinToPot] = valueList[pinToPot] * 5

    return valueReal

