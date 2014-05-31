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
    

    # Return to the beginning of all files
    for l in file_config:
        if type(l) is list:
            for f in l:
                f.seek(0)
        else:
            l.seek(0)

    filename = os.path.join(config[2], 'ewee_data.ods')
    ods = ezodf2.newdoc(
        doctype = 'ods', filename = '{f}'.format(f = filename))

        # Calculating number of columns necessary
    # +1 because number_analogue contains 0
    # +2 for coder and coder time
    n_columns = 1 + config[0] + 1 + config[6] + 1 + 2
    # Calculating number of lines
    buf = mmap.mmap(file_config[1].fileno(), 0)
    n_rows = 0
    while buf.readline():
        n_rows += 1
    sheet = ezodf2.Sheet('SHEET', size = (n_rows + 2, n_columns))
    ods.sheets += sheet

    # Writing sensors id in first row
    sheet['A1'].set_value('Horodatage')
    for i in range(config[0]):
        sheet['{letter}1'.format(
            letter = string.uppercase[i + 1])].set_value(config[1][i])
    # Add values id
    if config[6] > 0:
        for i in range(config[6]):
            sheet['{letter}1'.format(
                letter = string.uppercase[i + config[0] + 1])].set_value(config[5][i])
    # encoder timestamp
    sheet['{letter}1'.format(
        letter = string.uppercase[1 + config[0] + config[6]])].set_value('Horodatage enc')
    # Coder values
    sheet['{letter}1'.format(
        letter = string.uppercase[2 + config[0] + config[6]])].set_value('Encodeur')

    # timestamp writing
    buf = mmap.mmap(file_config[1].fileno(), 0)
    for i in range(n_rows):
        timestamp = float(buf.readline().decode('utf-8').rstrip())
        sheet['A{line}'.format(line = i + 2)].set_value(timestamp)
    
    # Analogue data writing
    for i, f in enumerate(file_config[0]):
        buf = mmap.mmap(f.fileno(), 0)
        for j in range(n_rows):
            val = float(buf.readline().decode('utf-8').rstrip())
            sheet['{letter}{line}'.format(
                letter = string.uppercase[i + 1], # +1 for time column
                line = j + 2)].set_value(val)
    
    # Additional datas writing
    for i, f in enumerate(file_config[2]):
        buf = mmap.mmap(f.fileno(), 0)
        for j in range(n_rows):
            val = float(buf.readline().decode('utf-8').rstrip())
            sheet['{letter}{line}'.format(
                letter = string.uppercase[i + 1 + config[0]],
                line = j + 2)].set_value(val)
    
    # Encoder writing
    buf = mmap.mmap(file_config[3].fileno(), 0)
    # Calculating number of lines for encoder:
    n_rows_encoder = 0
    while buf.readline():
        n_rows_encoder += 1
    # Writing coder timestamp
    buf.seek(0)
    for i in range(n_rows_encoder):
        val = 0.1*i
        sheet['{letter}{line}'.format(
            letter = string.uppercase[config[0] + 1 + config[6]],
            line = i + 2)].set_value(val)
    # Writing timestamp value
    for i in range(n_rows_encoder):
        val = float(buf.readline().decode('utf-8').rstrip())
        sheet['{letter}{line}'.format(
            letter = string.uppercase[config[0] + 2 + config[6]],
            line = i + 2)].set_value(val)

    ods.save()

    return 0
