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

def write_ods(dataDir, analogSensors):
    
    # définit le chemin du fichier
    filename = os.path.join(dataDir, 'ewee_data.ods')
    ods = ezodf2.newdoc(doctype = 'ods', filename = '{f}'.format(f = filename))
    
    
    
    #Ouverture des fichiers
    timePath = os.path.join(dataDir, 'timestamp')
    with open(timePath, 'r') as t:
        timestamp = [line.rstrip() for line in t]

    dataList = []
    for i in range(analogSensors):
        filePath = os.path.join(dataDir, "data_{i}".format(i = str(i)))
        with open(filePath, 'r') as di:
            dataList.append([line.rstrip() for line in di])
    
    # formatage des listes
    timestamp = map(float, timestamp)
    for i, elt in enumerate(dataList):
        dataList[i] = map(float, elt)
    
    sheet = ezodf2.Sheet('SHEET', size = (len(timestamp), analogSensors + 1))
    ods.sheets += sheet
    
    # écriture du timestamp
    for i, elt in enumerate(timestamp):
        sheet['A{line}'.format(line = i + 1)].set_value(elt)
        
    # écriture des données
    for i in range(analogSensors):
        dataListI = dataList[i]
        for j, elt in enumerate(dataListI):
            sheet['{letter}{line}'.format(
                letter = string.uppercase[i + 1],
                line = j + 1
                )].set_value(elt)
            
    ods.save()
    
