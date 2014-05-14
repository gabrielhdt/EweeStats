# -*- coding: utf-8 -*-
#
#  AnlogGraphThreads.py
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

import threading
import Queue
import time
import os
import sys
from pyfirmata import Arduino, util
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import graph
import pinselection
import ods
import collect_data
import clean_list


class AnalogGraphThreads(object):
    """
        Classe destinée aux threads de lecture des valeurs analogiques
        et de création du graph
    """

    def __init__(
        self, analogSensors, file_list, time_file, graph_name,
        datapath, sensor_id_list):
        """
        Constructeur de la classe : va créer transmit_is_ready
        pour contrôler l'état des threads et créer une queue d'un
        élément
        :param analogSensors: nombre de capteurs analogiques
        :type analogSensors: integer
        """

        self.transmit_is_ready = True
        self.queue_graph = Queue.Queue(maxsize=1)
        self.queue_clean = Queue.Queue(maxsize=1)
        self.queue_clean_return = Queue.Queue(maxsize=1)
        self.stop = False
        
        self.all_values = [[] for i in range(analogSensors)]
        self.timelist = []
        # Count how many times memory has been cleaned
        self.count_mem_clean = 1
        # Boolean used to init timestamp
        self.init_done = False

    def threadAnalogData(
        self, lcd, board, time_file, file_list, datapath):
        """
            Ce thread relève les valeurs analogiques, les stocke dans
            des fichiers et attent que le thread 2 soit prêt pour
            commencer le graph
        """
        ## Start listening ports
        #for i in range(self.analogSensors):
            #board.analog[i].enable_reporting()


        ## Wait for a valid value to avoid None
        #start = time.time()
        #while board.analog[0].read() is None:
                #print("nothing after {t}".format(
                    #t = time.time() - start))

        #print("first val after {t}".format(t = time.time() - start))
        #lcd.clear()
        #lcd.message("Debut des \nmesures")

        # init some more variables
        displayPin = 0
        timeDisplay = 0
    
        # Main loop
        while not lcd.buttonPressed(lcd.SELECT):
            
            # Calcule last display time
            time_last_display = time.time() - time_display
            
            # Buttons activity
            if time_last_display >= 0.25:
                display_pin = pinselection.display_selection(
                    number_sensors, lcd, displayPin)

            # Executed once
            if not self.init_done:
                timestampInit = time.time()
                self.init_done = True


            # Timestamping
            timestamp = time.time()
            timestamp = timestamp - timestampInit
            self.timelist.append(str(round(timestamp, 4))) # for pygal
            
            # Data reading and converting
            values_converted_instant = collect_data.collecting(
                board, self.sensor_id_list, self.analogSensors)
            
            # Data stocking
            for i in range(self.analogSensors):
                self.all_values[i].append(
                    round(values_converted_instant[i], 4))

            #print(value_list_instant)    # affiche dans la console les valeurs

            # Thread managing
            if self.transmit_is_ready == True:
                self.queue_graph.put(1)  # if ready, 1 in the queue

            #LCD displaying every 250ms
            if timeLastDisplay >= 0.25:
                lcd.clear()
                lcd.message("Pot {dp} :\n".format(dp = str(displayPin)))
                lcd.message(values_converted_instant[displayPin])
                timeDisplay = time.time() # for lagging
            print(self.timelist[-1])
            
            # Clean memory every 2 min or if list too big
            if float(self.timelist[-1]) >= 120*self.count_mem_clean:
                self.queue_clean.put(1)
                self.queue_clean_return.get(True)

        # Poweroff
        self.stop = True
        board.exit()
        lcd.clear()
        lcd.message('Ecriture des \nfichiers texte')
        # writing text data files
        for i, file in enumerate(self.file_list):
            for j in self.all_values[i]:
                file.write(str(j))
                file.write('\n')
        # writing timestamp file
        for i in self.timelist:
            self.time_file.write(i)
            self.time_file.write('\n')

        for i in self.file_list:
            i.close()
        self.time_file.close()
        lcd.clear()
        lcd.message('Ecrire ODS ?')
        lcd.clear()
        lcd.message('\nOui          Non')
        while not (lcd.buttonPressed(lcd.LEFT) or lcd.buttonPressed(lcd.RIGHT)):
            pass
        if lcd.buttonPressed(lcd.LEFT):
            lcd.clear()
            lcd.message("Ecriture du\nfichier ODS")
            ods.write_ods(
                self.datapath, self.analogSensors,
                self.all_values, self.timelist)
        lcd.clear()


    def threadGraph(self, analogSensors):
        """
            Thread construisant le graph :
            lit les valeurs, les formate comme il faut, configure puis
            crée le graph
        """

        while(not self.stop):    
            
            # waits until queue is full
            self.queue_graph.get(True)
            self.transmit_is_ready = False
            
            # Graph creation
            graph.create_graph(
                analogSensors, self.all_values,
                self.timelist, self.datapath, self.graph_name)

            # Task finished, now ready
            self.transmit_is_ready = True
    
    def thread_clean_mem(self):
        """
        Clean memory if list too big : copy lists into new ones to write
        them into a file then reset lists
        """
        while(not self.stop):
            self.queue_clean.get(True)
            time_temp = self.timelist
            values_temp = self.all_values
            self.timelist = []
            self.all_values = [[] for i in range(self.analogSensors)]
            self.count_mem_clean += 1
            #self.init_done = False
            print('Memory cleaned')
            self.queue_clean_return.put(1)
            
            clean_list.free_memory(
                values_temp, time_temp, self.file_list, self.time_file)
            del time_temp
            del values_temp
    
    

    def startThreads(self, analogSensors):
        """
            Sert à lancer les threads : les crée puis les lance
        """
        # Threads creation
<<<<<<< HEAD
        self.at = threading.Thread(target = )
        self.gt = threading.Thread(target = self.threadGraph, args=analogSensors)
=======
        self.at = threading.Thread(None, self.threadAnalogData, None)
        self.gt = threading.Thread(target=self.threadGraph, args=analogSensors)
>>>>>>> b25a7330ceb238be8bcbbdedaa647287b830b06b
        self.cmt = threading.Thread(None, self.thread_clean_mem, None)

        # Threads start
        self.at.start()
        self.gt.start()
        self.cmt.start()

