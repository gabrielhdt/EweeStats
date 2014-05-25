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
import coder
import RPi.GPIO as GPIO

class AnalogGraphThreads(object):
    '''
    Main class, creating the graph
    '''

    def __init__(self, number_sensors, number_add_values):
        """
        Constructeur de la classe : va créer transmit_is_ready
        pour contrôler l'état des threads et créer une queue d'un
        élément
        :param number_sensors: nombre de capteurs analogiques
        :type number_sensors: integer
        
        :param number_add_values: number of calculated variables
        :type number_add_values: integer
        """

        self.transmit_is_ready = True
        self.queue_graph = Queue.Queue(maxsize=1)
        self.queue_clean = Queue.Queue(maxsize=1)
        self.graph_coder_ready = True
        self.queue_graph_coder = Queue.Queue(maxsize=1)
        self.memory_busy = False
        self.stop = False
        
        self.all_values = [[] for i in range(number_sensors)]
        self.all_add_values = [[] for i in range(number_add_values)]
        self.coder_values = []
        self.timelist = []
        # Count how many times memory has been cleaned
        self.count_mem_clean = 1
        # Boolean used to init timestamp
        self.init_done = False

    def threadAnalogData(self, config, dev, file_config):
        """
        Main thread : loop reading and launches others threads to graph
        or clean mem
        :param config: tuple containing :
                        0 : number of analogue sensors
                        1 : sensors id
                        2 : save_dir
                        3 : graph_name
                        4 : pins to graph
                        5 : list of additional values id
                        6 : number of additional values
                        7 : encoder_pins
        :type config: tuple
        
        :param dev: tuple containing devices classes:
                        0 : lcd
                        1 : board (arduino)
                        2 : iter8
        :type dev: tuple
        
        :param file_config: tuple containing files
                0 - list of files for analogue datas
                1 - timestamp file
                2 - list of files for additional values
                3 - file for coder
        :type file_config: tuple
        """
        # Some shortcuts
        lcd = dev[0]
        board = dev[1]
        iter8 = dev[2]

        # init some more variables
        display_value = [0, 0] # 1st for type and 2nd for value
        time_display = 0
    
        # Main loop
        while not lcd.buttonPressed(lcd.SELECT):
            
            # Calculates last display time
            time_last_display = time.time() - time_display
            
            # Buttons activity
            if time_last_display >= 0.25:
                display_value = pinselection.display_selection(
                    config[0], config[6], lcd, display_value)

            # Timestamp init
            if not self.init_done:
                timestampInit = time.time()
                self.init_done = True

            # Timestamping
            timestamp = time.time()
            timestamp = timestamp - timestampInit
            self.timelist.append(str(round(timestamp, 4))) # for pygal
            
            # Data reading and converting
            values_converted_instant, add_values_instant = collect_data.collecting(
                board, config[1], config[0], config[5])
            
            # Data stocking
            for i in range(config[0]):
                self.all_values[i].append(
                    round(values_converted_instant[i], 4))
            for i in range(config[6]):
                self.all_add_values[i].append(
                    round(add_values_instant[i], 4))

            #print(value_list_instant)    # affiche dans la console les valeurs

            # Thread graph managing
            if self.transmit_is_ready:
                self.queue_graph.put(1)  # if ready, 1 in the queue

            #LCD displaying every 250ms
            if time_last_display >= 0.25:
                lcd.clear()
                if display_value[0] == 0:
                    lcd.message("Analogue : {dp} :\n".format(dp = str(display_value[1])))
                    lcd.message(values_converted_instant[display_value[1]])
                elif display_value[0] == 1:
                    lcd.message('Calculated : {dp} :\n'.format(dp = str(display_value[1])))
                    lcd.message(add_values_instant[display_value[1]])
                time_display = time.time() # for lagging
            
            # Clean memory every 2 min or if list too big
            if float(self.timelist[-1]) >= 120*self.count_mem_clean:
                self.queue_clean.put(1)
            while self.memory_busy:
                continue

        # Poweroff
        self.stop = True
        board.exit()
        lcd.clear()
        lcd.message('Ecriture des \nfichiers texte')
        # writing text data files
        for i, file in enumerate(file_config[0]):
            for j in self.all_values[i]:
                file.write(str(j))
                file.write('\n')
        for i, elt in enumerate(file_config[2]):
            for j in self.all_add_values[i]:
                elt.write(str(j))
                elt.write('\n')
        # writing timestamp file
        for i in self.timelist:
            file_config[1].write(i)
            file_config[1].write('\n')

        for i in file_config[0]:
            i.close()
        file_config[1].close()
        for i in file_config[2]:
            i.close()
        file_config[3].close()
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
            graph.create_graph(config, self.all_values,self.all_add_values, self.timelist)

            # Task finished, now ready
            self.transmit_is_ready = True
    
    def thread_clean_mem(
        self, number_sensors, number_add_sensors, file_config):
        """
        Clean memory if list too big : copy lists into new ones to write
        them into a file then reset lists
        """
        while(not self.stop):
            self.queue_clean.get(True)
            self.memory_busy = True
            time_temp = self.timelist
            values_temp = self.all_values
            add_values_temp = self.all_add_values
            coder_values_temp = self.coder_values
            self.timelist = []
            self.all_values = [[] for i in range(number_sensors)]
            self.all_add_values = [[] for i in range(number_add_sensors)]
            self.coder_values = []
            self.count_mem_clean += 1
            #self.init_done = False
            print('Memory cleaned')
            self.memory_busy = False
            
            clean_list.free_memory(
                values_temp, time_temp, add_values_temp, coder_values_temp, file_config[0],
                file_config[1], file_config[2], file_config[3])
            del time_temp
            del values_temp
            del add_values_temp
    
    def thread_coder(self, encoder_pins):
        '''
        Thread for coder using interrupts and all that mess
        :returns: ewee's speed in km/h
        :rtype: float
        '''
        GPIO.add_event_detect(encoder_pins[0], GPIO.RISING, callback=coder.update_encoder)
        GPIO.add_event_detect(encoder_pins[1], GPIO.RISING, callback=coder.update_encoder)
        
        coder_time = time.time()
        circonference = 0.6283
        
        while not self.stop:
            coder_counter = time.time() - coder_time
            if coder_counter >= 0.1:
                speed = coder.coder(circonference)
                coder_time = time.time()
                self.coder_values.append(speed)
                if self.graph_coder_ready:
                    self.queue_graph_coder.put(True)
                #print(speed)
    
    def thread_graph_coder(self, config):
        '''
        Thread making a graph for coder only
        '''
        interval = 0.1
        while not self.stop:
            self.queue_graph_coder.get(True)
            self.graph_coder_ready = False
            
            graph.coder(config, self.coder_values, interval)
            
            self.graph_coder_ready = True
    

    def startThreads(
        self, config, dev, file_config):
        '''
        Creates and starts threads
        :param config: tuple containing :
                0 - number of sensors
                1 - list id of sensors (indice is pin and name is type)
                2 - save directory
                3 - name of the graph
                4 - pins to be graphed
                5 - list of additional values id
                6 - number of additional_values
                7 - list of two pins for encoder
        :type config: tuple
        
        :param dev: tuple containing dev info:
                0 - lcd
                1 - arduino
                2 - iter8
        :type dev: tuple
        
        :param file_config: tuple containing files
                0 - list of files for analogue datas
                1 - timestamp file
                2 - list of files for additional values
                3 - file for coder
        :type file_config: tuple
        '''
        # Threads creation

        self.at = threading.Thread(
            target = self.threadAnalogData,
            args = (config, dev, file_config)
            )
        
        self.gt = threading.Thread(
            target=self.threadGraph,
            args = (config,)
            )
        
        self.cmt = threading.Thread(
            target = self.thread_clean_mem,
            args = (config[0], config[6], file_config)
            )
            
        self.ct = threading.Thread(
            target = self.thread_coder,
            args = (config[7],)
            )
        
        self.gct = threading.Thread(
            target = self.thread_graph_coder,
            args = (config,)
            )

        # Threads start
        self.at.start()
        self.gt.start()
        self.cmt.start()
        self.ct.start()
        self.gct.start()

