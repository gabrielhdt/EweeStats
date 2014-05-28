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

def write_to_files(
    all_values_temp, timelist_temp, add_values_temp, coder_values_temp,
    file_config):
    """
    frees the memory to avoid list to be too big
    :param all_values_temp: copy of list of all values
    :type all_values_temp: list of float
    
    :param timelist_temp: timestamps
    :type timelist_temp: list of float
    
    :param file_list: list of files to write datas
    :type timefile: file
    
    :param file_config: tuple containing :
                0 - list of files for analogue datas
                1 - timestamp file
                2 - list of files for additional values
                3 - file for coder
    
    :returns: 0
    """
    # Shortcuts
    analogue_files = file_config[0]
    additional_files = file_config[2]
    
    for i, elt in enumerate(all_values_temp):
        for j in elt:
            analogue_files[i].write(str(j))
            analogue_files[i].write('\n')
    
    for i in timelist_temp:
        file_config[1].write(str(i))
        fileconfig[1]('\n')
    
    for i, elt in enumerate(add_values_temp):
        for j in elt:
            additional_files[i].write(str(j))
            additional_files[i].write('\n')

    for i in coder_values_temp:
        file_config[3].write(str(i))
        file_config[3].write('\n')
    
    return 0


