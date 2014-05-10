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

def free_memory(all_values_temp, timelist_temp, filelist, timefile):
    """
    :param list_all_values: list of all values
    :type list_all_values: list
    
    :returns: 0
    """
    for i, elt in enumerate(all_values):
        for j in elt:
            fpath = filelist[i]
            with open(fpath, 'a') as f:
                f.write(str(j))
                f.write('\n')
    
    with open(timefile, 'a') as t:
        for i in timelist_temp:
            t.write(str(i))
            t.write('\n')
    
    return 0


