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

    def __init__(self, number_sensors):
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
        
        self.all_values = [[] for i in range(number_sensors)]
        self.timelist = []
        # Count how many times memory has been cleaned
        self.count_mem_clean = 1
        # Boolean used to init timestamp
        self.init_done = False

    def threadAnalogData(
        self, config, dev, file_list, time_file):
        """
        Main thread : loop reading and launches others threads to graph
        or clean mem
        :param config: tuple containing :
                        0 : number of analogue sensors
                        1 : sensors id
                        2 : save_dir
                        3 : graph_name
                        4 : pins to graph
        :type config: tuple
        
        :param dev: tuple containing devices classes:
                        0 : lcd
                        1 : board (arduino)
                        2 : iter8
        :type dev: tuple
        
        :param file_list: list of files in which we write
        :type file_list: list of files
        
        :param time_file: file to write timestamp
        :type time_file: file
        """
        # Some shortcuts
        lcd = dev[0]
        board = dev[1]
        iter8 = dev[2]

        # init some more variables
        display_pin = 0
        time_display = 0
    
        # Main loop
        while not lcd.buttonPressed(lcd.SELECT):
            
            # Calculates last display time
            time_last_display = time.time() - time_display
            
            # Buttons activity
            if time_last_display >= 0.25:
                display_pin = pinselection.display_selection(
                    config[0], lcd, display_pin)

            # Timestamp init
            if not self.init_done:
                timestampInit = time.time()
                self.init_done = True

            # Timestamping
            timestamp = time.time()
            timestamp = timestamp - timestampInit
            self.timelist.append(str(round(timestamp, 4))) # for pygal
            
            # Data reading and converting
            values_converted_instant, additional_values = collect_data.collecting(
                board, config[1], config[0])
            
            # Data stocking
            for i in range(config[0]):
                self.all_values[i].append(
                    round(values_converted_instant[i], 4))

            #print(value_list_instant)    # affiche dans la console les valeurs

            # Thread managing
            if self.transmit_is_ready == True:
                self.queue_graph.put(1)  # if ready, 1 in the queue

            #LCD displaying every 250ms
            if time_last_display >= 0.25:
                lcd.clear()
                lcd.message("Pot {dp} :\n".format(dp = str(display_pin)))
                lcd.message(values_converted_instant[display_pin])
                time_display = time.time() # for lagging
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
        for i, file in enumerate(file_list):
            for j in self.all_values[i]:
                file.write(str(j))
                file.write('\n')
        # writing timestamp file
        for i in self.timelist:
            time_file.write(i)
            time_file.write('\n')

        for i in file_list:
            i.close()
        time_file.close()
        lcd.clear()
        lcd.message('Ecrire ODS ?')
        lcd.clear()
        lcd.message('\nOui          Non')
        # Wait for entry
        while not (lcd.buttonPressed(lcd.LEFT) or lcd.buttonPressed(lcd.RIGHT)):
            pass
        if lcd.buttonPressed(lcd.LEFT):
            lcd.clear()
            lcd.message("Ecriture du\nfichier ODS")
            ods.write_ods(
                config[2], config[0],
                self.all_values, self.timelist)
        lcd.clear()


    def threadGraph(self, config):
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
            graph.create_graph(config, self.all_values, self.timelist)

            # Task finished, now ready
            self.transmit_is_ready = True
    
    def thread_clean_mem(self, number_sensors):
        """
        Clean memory if list too big : copy lists into new ones to write
        them into a file then reset lists
        """
        while(not self.stop):
            self.queue_clean.get(True)
            time_temp = self.timelist
            values_temp = self.all_values
            self.timelist = []
            self.all_values = [[] for i in range(number_sensors)]
            self.count_mem_clean += 1
            #self.init_done = False
            print('Memory cleaned')
            self.queue_clean_return.put(1)
            
            clean_list.free_memory(
                values_temp, time_temp, self.file_list, self.time_file)
            del time_temp
            del values_temp
    
    

    def startThreads(self, config, dev, file_list, time_file):
        """
            Sert à lancer les threads : les crée puis les lance
        """
        # Threads creation

        self.at = threading.Thread(
            target = self.threadAnalogData,
            args = (config, dev, file_list, time_file))
        
        self.gt = threading.Thread(
            target=self.threadGraph,
            args = (config,))
        
        self.cmt = threading.Thread(
            target = self.thread_clean_mem,
            args = (config[0],))

        # Threads start
        self.at.start()
        self.gt.start()
        self.cmt.start()

