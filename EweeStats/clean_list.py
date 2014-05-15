# -*- coding: utf-8 -*-
#
#  clean_list.py
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

import os
import sys
import time

def free_memory(all_values_temp, timelist_temp, file_list, timefile):
    """
    frees the memory to avoid list to be too big
    :param all_values_temp: copy of list of all values
    :type all_values_temp: list of float
    
    :param timelist_temp: timestamps
    :type timelist_temp: list of float
    
    :param file_list: list of files to write datas
    :type timefile: file
    
    :returns: 0
    """
    time.sleep(1)
    print(type(file_list[0]))
    time.sleep(1)
    for i, elt in enumerate(all_values_temp):
        fpath = file_list[i]
        for j in elt:
            fpath.write(str(j))
            fpath.write('\n')
    
    for i in timelist_temp:
        timefile.write(str(i))
        timefile.write('\n')
    
    return 0


