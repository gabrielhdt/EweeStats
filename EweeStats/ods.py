# -*- encoding: utf-8 -*-
#
#  ods.py
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


import ezodf2
import os
import sys
import string
import mmap

def write_ods(config, file_config):
    '''
    Writes ods file
    :param config:tuple containing :
                0 : number of analogue sensors
                1 : sensors id
                2 : save_dir
                3 : graph_name
                4 : pins to graph
                5 : list of additional values id
                6 : number of additional values
                7 : encoder_pins
    :param file_config: tuple containing files
                0 - list of files for analogue datas
                1 - timestamp file
                2 - list of files for additional values
                3 - file for coder
    :type file_config: tuple
    '''
    

    filename = os.path.join(config[2], 'ewee_data.ods')
    ods = ezodf2.newdoc(
        doctype = 'ods', filename = '{f}'.format(f = filename))
    
    # Calculating number of columns necessary
    # +1 because number_analogue contains 0
    # +2 for coder and coder time
    n_columns = config[0] + 1 + config[6] + 1 + 2
    n_rows = count_lines(file_config[1])
    sheet = ezodf2.Sheet('SHEET', size = (n_rows, n_columns))
    ods.sheets += sheet
    
    # timestamp writing
    buf = mmap.mmap(file_config[1].fileno(), 0)
    for i in range(n_rows):
        timestamp = float(buf.readline().decode('utf-8').rstrip())
        sheet['A{line}'.format(line = i + 2)].set_value(timestamp)
    
    # Analogue data writing
    for f in file_config[0]:
        buf = mmap.mmap(f.fileno(), 0)
        for j in range(n_rows):
            val = float(buf.readline().decode('utf-8').rstrip())
            sheet['{letter}{line}'.format(
                letter = string.uppercase[i + 1],
                line = j + 2)].set_value(val)
    
    # Additional datas writing
    for f in file_config[2]:
        buf = mmap.mmap(f.fileno(), 0)
        for j in range(n_rows):
            val = float(buf.readline().decode('utf-8').rstrip())
            sheet['{letter}{line}'.format(
                letter = string.uppercase[i + 1],
                line = j + 2)].set_value(val)

    ods.save()
    
def count_lines(file_to_read):
    '''Count lines of a file'''
    buf = mmap.mmap(file_to_read.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines
    
