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
import pygal
from pyfirmata import Arduino, util
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import graph
import pinselection
import ods
import convert_data
import itertools


class AnalogGraphThreads(object):
    """
        Classe destinée aux threads de lecture des valeurs analogiques
        et de création du graph
    """

    def __init__(self, analogSensors):
        """
        Constructeur de la classe : va créer transmit_is_ready
        pour contrôler l'état des threads et créer une queue d'un
        élément
        :param analogSensors: nombre de capteurs analogiques
        :type analogSensors: integer
        """

        self.transmit_is_ready = True
        self.my_queue = Queue.Queue(maxsize=1)
        self.stop = False
        self.analogSensors = analogSensors
        
        self.listValueLists = [[] for i in range(analogSensors)]
        self.timelist = []

    def threadAnalogData(self):
        """
            Ce thread relève les valeurs analogiques, les stocke dans
            des fichiers et attent que le thread 2 soit prêt pour
            commencer le graph
        """
        # Init affichage lcd
        lcd = Adafruit_CharLCDPlate()
        lcd.clear()

        # Booléen indiquant l'état de l'initialisation
        # pour l'horodatage et le pinselection
        initDone = False
        # Liste des valeurs
        valueList = [0.0 for i in range(self.analogSensors)]

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

        # Création fichier graph
        graphName = 'EweeGraph.svg'
        # Si le fichier à la racine web existe, on le supprime
        if os.path.isfile(os.path.join('/var/www', graphName)):
                os.remove(os.path.join('/var/www', graphName))
        # Puis on crée le lien
        os.symlink(os.path.join(newpath, graphName), os.path.join('/var/www', graphName))



        # Ouvre un fichier par pin analog en écriture nommé data_X 
        fileList = []       # liste contenant tous les fichiers
        for i in range(self.analogSensors):
            # Création d'un nom de fichier avec indexe i (data_0, data_1 ...)
            filename = "data_{i}".format(i = str(i))
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
        for i in range(self.analogSensors):
            board.analog[i].enable_reporting()


        # Wait for a valid value to avoid None
        start = time.time()
        while board.analog[0].read() is None:
                print "nothing after {t}".format(t = time.time() - start)

        print "first val after {t}".format(t = time.time() - start)
        lcd.clear()
        lcd.message("Debut des \nmesures")

        # initialisation de variables
        displayPin = 0
        timeDisplay = 0

        ###### FIN INIT ########################################################
        
        
        # Boucle principale, continue tant qu'on appuie pas sur SELECT
        while lcd.buttonPressed(lcd.SELECT) != 1:
            
            # Calcul du dernier affichage
            timeLastDisplay = time.time() - timeDisplay
            
            # relève l'état des boutons
            if timeLastDisplay >= 0.25:
                displayPin = pinselection.display_selection(
                    self.analogSensors, lcd, displayPin)


            #### INIT TIMESTAMP ####
            if initDone is False:      # Pour n'initialiser qu'une seule fois le timestamp
                timestampInit = time.time()
                initDone = True            # Booléen indiquant que timestampInit a été initialisé
            #### FIN INIT TIMESTAMP ####

            #### CREATION DU TIMESTAMP ####
            timestamp = time.time()             # Lecture du temps
            timestamp = timestamp - timestampInit   # Différence entre le temps initial et le temps de la prise
            # horodatage en char pour le graph pygal
            self.timelist.append(str(round(timestamp, 4)))

            #### TRAITEMENT DES DONNEES ####
            # Version en deux boucles :
            # diminue le décalage de temps entre chaque lecture de données
            for i in range(self.analogSensors):
                valueList[i] = board.analog[i].read()   # lecture et enregistrement dans la liste

            # Conversion des données
            valueList = convert_data.convert(valueList)
            # Stockage des données dans la liste
            for i in range(self.analogSensors):
                self.listValueLists[i].append(round(valueList[i], 4))

            #print(valueList)    # affiche dans la console les valeurs

            #### GESTION DES THREADS ####
            # Regarde si le thread 2 est prêt
            if self.transmit_is_ready == True:
                self.my_queue.put(1)        # s'il est prêt, on met 1 dans la queue

            #### AFFICHAGE DES VALEURS SUR LCD ####
            if timeLastDisplay >= 0.25:                     # Si le temps excède les 250ms
                lcd.clear()
                lcd.message("Pot {dp} :\n".format(dp = str(displayPin)))
                lcd.message(valueList[displayPin])
                timeDisplay = time.time()                   # Enregistre le moment d'affichage

        #### EXTINCTION ####
        self.stop = True    # On dit au thread 2 de s'arrêter
        lcd.message('Ecriture des \nfichiers texte')
        # écriture fichier texte données
        for i, file in enumerate(fileList):
            for j in self.listValueLists[i]:
                file.write(str(j))
                file.write('\n')
        # écriture fichier texte horodatage
        for i in self.timelist:
            timeFile.write(i)
            timeFile.write('\n')
            
        for fi in fileList:
            fi.close()
        timeFile.close()
        board.exit()
        lcd.clear()
        lcd.message("Ecriture du\nfichier ODS")
        ods.write_ods(newpath, self.analogSensors)
        lcd.clear()


    def threadGraph(self):
        """
            Thread construisant le graph :
            lit les valeurs, les formate comme il faut, configure puis
            crée le graph
        """
        # Tant que le thread 1 ne dit pas de s'arrêter on boucle
        while(not self.stop):    
            
            # gestion du démarrage du thread
            # attend jusqu'à ce que la queue se remplisse
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

            graphName = 'EweeGraph.svg'
            
            # Création du graph
            graph.create_graph(self.analogSensors, self.listValueLists,
                self.timelist, newpath, graphName)

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

