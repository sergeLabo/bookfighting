#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

# Copyright (C) Labomedia April 2013
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

'''
To use this script with another project, change handler for exemple:
    To receive all message, without sub-messsage:
        self.receiver.addCallback("/*", some_handler)
    or, with touchosc, for example:
        self.receiver.addCallback("/1/*", some_handler)
    and create some_handler
'''

import os
import sys
import threading
from time import time, sleep

try:
    from txosc import async, dispatch, osc
except ImportError:
    print "Import Error txosc: txosc devrait ètre dans le dossier du script"

try:
    from twisted.internet import reactor
except ImportError:
    print "Import Error twisted.internet."
    print "On Ubuntu:"
    print " sudo apt-get install python-twisted"
    pass

# Import du module avec le dictionnaire qui gère les datas
import OscDict

class UDPSender(object):
    ''' Envoi de datas à Blender en UDP
    '''
    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.client = async.DatagramClientProtocol()
        self._client_port = reactor.listenUDP(0, self.client)
        print("Sending on: %s : %s" % (self.host, self.port))

    def send_message(self, message):
        self.client.send(message, (self.host, self.port))

class UDPReceiver(object):
    ''' Reception des datas de tous les téléphones en UDP '''
    def __init__(self, port):
        self.port = port
        self.receiver = dispatch.Receiver()
        self._server_port = reactor.listenUDP(self.port, async.DatagramServerProtocol(self.receiver))
        print("Réception de l' UDP sur: %s : %s" % (host, self.port))

        # quit
        self.receiver.addCallback("/quit", self.quit_handler)

        # If Blender is not running, kill the server
        #self.receiver.addCallback("/I_am_running", server_instance.I_am_running_handler)

        # TouchOSC
        # "/*/xy": [0,0]
        self.receiver.addCallback("/*/xy", server_instance.player_data_handler_xy)
        # "/accxyz": [0,0,0]
        self.receiver.addCallback("/accxyz", server_instance.player_data_handler_accxyz)

        # ControlOSC
        # "/multi": [0,0] ?
        self.receiver.addCallback("/multi/1", server_instance.player_data_handler_multi)
        # "/acc": [0,0,0] ?
        #self.receiver.addCallback("/acc", server_instance.player_data_handler_acc)

        # AndOSC
        # "/touch": [0, 0] à [600, 1200]
        self.receiver.addCallback("/touch", server_instance.player_data_handler_touch)
        # "/acc": [-9,-9,-9] à [9,9,9]
        self.receiver.addCallback("/acc", server_instance.player_data_handler_acc)

    def quit_handler(self, message, address):
        print("Quit : Reception de  %s envoyé par %s" % (message, address))
        print("Fin du script server.py")
        #  Le message quit envoyé par blender stoppe ce script
        # Blender kill les processus python2.7 au lancement pour être sûr qu'il n'y a qu'un seul script qui tourne
        reactor.stop()
        os._exit(0)

class server_main(object):
    ''' Le server qui reçoit les datas des téléphones
        et envoie à Blender les datas mis en forme toutes les 0.016 secondes
    '''
    def __init__(self, port_in, port_out, host):
        self.port_in = port_in
        self.port_out = port_out
        self.host = host
        self.t_zero = time()

    def game_server(self):
        '''Le serveur tourne et gère avec le module OscDict'''
        self.gameDict = OscDict.allOscData()
        print("Game Server of Book Fighting\n Press q + Enter to quit")
        # Set instance
        self.udp_sender = UDPSender(self.port_out, self.host)
        self.udp_receiver = UDPReceiver(self.port_in)
        reactor.run()

    def player_data_handler_xy(self, message, address):
        '''Fonction appelée par le receiver'''
        self.gameDict.insert_data_in_dict_xy(message.getValues(), address)

    def player_data_handler_multi(self, message, address):
        '''Fonction appelée par le receiver'''
        self.gameDict.insert_data_in_dict_multi(message.getValues(), address)

    def player_data_handler_touch(self, message, address):
        '''Fonction appelée par le receiver'''
        self.gameDict.insert_data_in_dict_touch(message.getValues(), address)

    def player_data_handler_accxyz(self, message, address):
        '''Fonction appelée par le receiver'''
        self.gameDict.insert_data_in_dict_accxyz(message.getValues(), address)

    def player_data_handler_acc(self, message, address):
        '''Fonction appelée par le receiver'''
        self.gameDict.insert_data_in_dict_acc(message.getValues(), address)

    def I_am_running_handler(self, message, address):
        '''Toutes les secondes, ce message doit être reçu'''
        if time() - self.t_zero > 1.1:
            ##reactor.stop()
            ##os._exit(0)
            pass
        else:
            self.t_zero = time()

    def delete_disconnected(self):
        '''Suppression des déconnectés dans le dictionnaire toutes les 2 secondes'''
        while True:
            sleep(2)
            # Destruction toutes les 2 secondes
            self.gameDict.delete_disconnected_player()

            # Impression de messages envoyés pour debug
            msg_for_blender = self.gameDict.create_blender_msg()
            print("Extrait des messages envoyés: %s" % (self.msg_for_blender))
            print("Game Server : Appuyer sur q + Entrée pour arrèter le script")

    def sendToBlender(self):
        '''Fréquence d'envoi à 60 Hz, Blender tourne à 60 fps'''
        while True:
            sleep(0.015)
            self.msg_for_blender = self.gameDict.create_blender_msg()
            self.udp_sender.send_message(self.msg_for_blender)

    def reset_handler(self, message, address):
        '''Remize à zéro du dictionnaire'''
        print ("Reset ...")
        self.gameDict.reset_data()

def thread_keyboard():
    '''Attente de l'appui sur q'''
    while True:
        c = sys.stdin.read(1)
        if c == 'q':
            print("Exit")
            os._exit(0)

if __name__ == "__main__":
    # localhost
    host = '127.0.0.1'

    # Port d'écoute des téléphones:
    port_in = 9000

    # Port d'envoi à blender en local
    port_out = 8000

    t0 = 0
    pulse = 0

    # Conversation
    print "Book Fighting by Labomedia \n\n"
    print "        Thank's to Yves"
    print "See http://bookfighting.blogspot.fr/"

    print "\n", "Incomming Local and Port IP:"
    print "IP =", host, "Port = ", port_in, "\n"

    # Création du serveur
    server_instance = server_main(port_in, port_out, host)

    ### Only if this script is run in console
    ##thread1 = threading.Thread(target=thread_keyboard)
    ##thread1.start()

    # Envoi en continu
    thread2 = threading.Thread(target=server_instance.sendToBlender)
    thread2.start()

    # Suppression toutes les 2 secondes
    thread3 = threading.Thread(target=server_instance.delete_disconnected)
    thread3.start()

    # Lancement du serveur
    server_instance.game_server()
