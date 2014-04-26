#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  EweeStats.py
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

import threading
import Queue
import time
import os
import sys
import pygal
from pyfirmata import Arduino, util
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import EweeStats.graph
import EweeStats.pinselection

# Variables globales :
# définissant le nombre de capteurs branchés en analogique
analogSensors = 2


class AnalogGraphThreads():
    """
        Classe destinée aux threads de lecture des valeurs analogiques
        et de création du graph
    """

    def __init__(self):
        """
            Constructeur de la classe : va créer transmit_is_ready
            pour contrôler l'état des threads et créer une queue d'un
            élément
        """

        self.transmit_is_ready = True
        self.my_queue = Queue.Queue(maxsize=1)
        self.stop = False

    def threadAnalogData(self):
        """
            Ce thread relève les valeurs analogiques, les stocke dans
            des fichiers et attent que le thread 2 soit prêt pour
            commencer le graph
        """
        # Init affichage lcd
        lcd = Adafruit_CharLCDPlate()
        lcd.clear()

        # Nombre de capteurs analogiques :
        global analogSensors
        # Booléen indiquant l'état de l'initialisation de l'instant 0 pour l'horodatage
        timestampInitDone = False
        # Liste des valeurs
        valueList = []                  # On crée une liste vide
        for i in range(analogSensors):
            valueList.append(0.000)     # On rajoute autant de 0 flottants qu'il y a de capteurs

        # Init Arduino et iterateur
        lcd.message("Connection de \nl'Arduino ...")
        board = Arduino('/dev/ttyACM0')
        lcd.clear()
        print('Arduino connected')
        lcd.message("Arduino connecte !")
        # Création itérateur
        iter8 = util.Iterator(board)
        iter8.start()

        #################################
        #   CREATION DES FICHIERS   #
        #################################
        # Répertoire de sortie
        # création du dossier de sauvegarde
        # répertoire racine
        dataDir = '/home/pi'
        # nom dossier sauvegarde
        outDir = 'ewee_data'
        # création du dossier
        newpath = os.path.join(dataDir, outDir)
        # Si le dossier n'existe pas, le créer
        if not os.path.exists(newpath): os.makedirs(newpath)

        


        # Ouvre un fichier par pin analog en écriture nommé data_X 
        fileList = []       # liste contenant tous les fichiers
        for i in range(analogSensors):
            # Création d'un nom de fichier avec indexe i (data_0, data_1 ...)
            filename = "data_%s"%str(i)
            # définition du chemin vers lequel les fichiers seront enregistrés
            filepath = os.path.join(newpath, filename)
            file = open(filepath, 'w+') # création de chaque fichier
            fileList.append(file)   # On ajoute le fichier à la liste

        filepath = os.path.join(newpath, "timestamp")   # refait le chemin
        timeFile = open(filepath, 'w+')                 # créé le fichier
        print(fileList)
        lcd.clear()
        lcd.message("fichiers ouvert")

        #################################

        # Commence l'écoute des ports nécessaires
        for i in range(analogSensors):
            board.analog[i].enable_reporting()


        # Wait for a valid value to avoid None
        start = time.time()
        while board.analog[0].read() is None:
                print "nothing after {0}".format(time.time() - start)

        print "first val after {0}".format(time.time() - start)
        lcd.clear()
        lcd.message("Debut des \nmesures")

        displayPin = 0  # Initialisation de la variable pour le choix des pins
        timeDisplay = 0 # Init variable pour le retardement de l'affichage

        ###### FIN INIT ########################################################

        while lcd.buttonPressed(lcd.SELECT) != 1: # Continue tant qu'on appuie pas sur SELECT

            # Choix du pin a afficher selection avec les boutons
            #if lcd.buttonPressed(lcd.UP) == 1:      # si on appuie sur le bouton up, on affiche le pin A0
                #print('--UP PRESSED--')
                #displayPin = 0
            #elif lcd.buttonPressed(lcd.DOWN) == 1:  # si on appuie sur le bouton down, on affiche le pin A1
                #print('--DOWN PRESSED--')
                #displayPin = 1
                
        EweeStats.pinselection.display_selection(analogSensors)


            #### INIT TIMESTAMP ####
            if timestampInitDone is False:      # Pour n'initialiser qu'une seule fois le timestamp
                timestampInit = time.time()
                timestampInitDone = True            # Booléen indiquant que timestampInit a été initialisé
            #### FIN INIT TIMESTAMP ####

            #### CREATION DU TIMESTAMP ####
            timestamp = time.time()             # Lecture du temps
            timestamp = timestamp - timestampInit   # Différence entre le temps initial et le temps de la prise
            timeFile.write(str(round(timestamp, 4)))              # écriture dans le fichier de temps
            timeFile.write('\n')

            #### TRAITEMENT DES DONNEES ####
            # Version en deux boucles :
            # diminue le décalage de temps entre chaque lecture de données
            for i, file in enumerate(fileList):         # boucle lecture
                valueList[i] = board.analog[i].read()   # lecture et enregistrement dans la liste

            print(valueList)                            # affiche dans la console les valeurs
            for i, file in enumerate(fileList):         # boucle écriture
                file.write(str(valueList[i]))              # écriture valeur
                file.write('\n')

            #### GESTION DES THREADS ####
            # Regarde si le thread 2 est prêt
            if self.transmit_is_ready == True:
                self.my_queue.put(1)        # s'il est prêt, on met 1 dans la queue

            #### AFFICHAGE DES VALEURS SUR LCD ####
            timeLastDisplay = time.time() - timeDisplay     # Calcul du temps du dernier affichage
            if timeLastDisplay >= 0.25:                     # Si le temps excède les 250ms
                lcd.clear()
                lcd.message("Pot %s :\n"%(str(displayPin))) # Affiche le message
                lcd.message(valueList[displayPin] * 10)
                timeDisplay = time.time()                   # Enregistre le moment d'affichage

        #### EXTINCTION ####
        self.stop = True                    # On dit au thread 2 de s'arrêter
        lcd.message("Fermeture des \nlogs")
        for fi in fileList:
            fi.close()
        timeFile.close()
        lcd.clear()
        lcd.message("Extinction ...")
        time.sleep(1)
        lcd.clear()
        board.exit()


    def threadGraph(self):
        """
            Thread construisant le graph :
            lit les valeurs, les formate comme il faut, configure puis
            crée le graph
        """
        global analogSensors
        while(not self.stop):               # Tant que le thread 1 ne dit pas de s'arrêter on boucle
            # gestion du démarrage du thread : attend jusqu'à ce que la queue se remplisse
            self.my_queue.get(True)
            # Quand la queue est remplie, le thread passe en état occupé
            self.transmit_is_ready = False
            
            # définissant le répertoire de sortie
            # création du dossier de sauvegarde
            # répertoire racine
            dataDir = '/home/pi'
            # nom dossier sauvegarde
            outDir = 'ewee_data'
            # création du dossier
            newpath = os.path.join(dataDir, outDir)
            
            EweeStats.graph.create_graph(analogSensors, newpath)

            # Tâche terminée, le thread 2 est prêt
            self.transmit_is_ready = True



    def startThreads(self):
        """
            Sert à lancer les threads : les crée puis les lance
        """
        # Création des threads
        self.at = threading.Thread(None, self.threadAnalogData, None)
        self.gt = threading.Thread(None, self.threadGraph, None)

        # Lancement des threads
        self.at.start()
        self.gt.start()

if __name__ == '__main__':
        data2Graph = AnalogGraphThreads()
        data2Graph.startThreads()
