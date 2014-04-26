# -*- encoding: utf-8 -*-
#
#  ods.py
#  
#  Copyright 2014 Gabriel Hondet <gabrielhondet@gmail.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

import ezodf2
import os

def write_ods(dataDir):
    
    # définit le chemin du fichier
    filename = os.path.join(dataDir, 'ewee_data.ods')
    ods = ezodf2.newdoc(doctype = 'ods', filename = '{f}'.format(f = filename))
    
    sheet = ezodf2.Sheet('SHEET', size = (10, 10))
    ods.sheets += sheet
    
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
    timestamp = map(int, timestamp)
    for i, elt in enumerate(dataList):
        dataList[i] = map(int, elt)
        
    for i, elt in enumerate(timestamp):
        sheet['A{line}'.format(line = i + 1)].set_value(elt)
        
        
    ods.save()
    
