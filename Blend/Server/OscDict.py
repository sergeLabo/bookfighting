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
## OscDict.py

'''
Ce module gère toutes les datas reçues des téléphones, dans un dictionnaire.
'''

try:
    from txosc import  osc
except ImportError:
    print "Import Error txosc: txosc devrait ètre dans le dossier du script"
    pass

from time import time

class allOscData(object):
    '''Create pool Dictionnary with all datas from all smartphone'''
    def __init__(self):
        self.pool = {}
        self.ACTA = {}

    def insert_data_in_dict_xy(self, message, address):
        # Ajout dans le dictionnaire de x, y si la clé existe
        # Les accélérations vont créer la clé forcément avant
        if address in self.pool:
            # inversion du sens: y = 0 est en haut , 1 en bas
            self.pool[address][1] = [message[0], 1 - message[1]]

    def insert_data_in_dict_multi(self, message, address):
        # Ajout dans le dictionnaire de x, y si la clé existe
        # Les accélérations vont créer la clé forcément avant
        if address in self.pool:
            # inversion du sens: y = 0 est en haut , 1 en bas
            self.pool[address][1] = [message[0], 1 - message[1]]

    def insert_data_in_dict_touch(self, message, address):
        # Ajout dans le dictionnaire de x, y si la clé existe
        # Les accélérations vont créer la clé forcément avant
        if address in self.pool:
            x = message[0]/480
            if x < 0:
                x = 0
            if x > 1:
                x = 1
            y = message[1]/800
            if y < 0:
                y = 0
            if y > 1:
                y = 1
            # inversion du sens: y = 0 est en haut , 1 en bas
            self.pool[address][1] = [x, 1 - y]

    def insert_data_in_dict_accxyz(self, message, address):
        # Ajout dans le dictionnaire des accélérations qui doivent ètre envoyées en continu
        # si la clé existe
        if address in self.pool:
            self.pool[address][0] = message
        # si la clé n'existe pas
        else:
            self.pool[address] = [ [0, 0, 0] , [0, 1] ]
            self.pool[address][0] = message
        # add in dict to control the web
        self.ACTA[address] = time()

    def insert_data_in_dict_acc(self, message, address):
        # Ajout dans le dictionnaire des accélérations qui doivent ètre envoyées en continu
        # si la clé existe
        if address in self.pool:
            self.pool[address][0] = message
        # si la clé n'existe pas
        else:
            self.pool[address] = [ [0, 0, 0] , [0, 1] ]
            self.pool[address][0] = message
        # add in dict to control the web
        self.ACTA[address] = time()

    def delete_disconnected_player(self):
        # Supprime les clés de joueurs qui n'envoie plus de data au delà de 1 s
        for addr, t in self.ACTA.items():
            if time() -t > 1:
                del self.pool[addr]
                del self.ACTA[addr]
                print "Deleted in ACTA, in pool, and I kill the player: ", addr

    def create_blender_msg(self):
        # Crée le message envoyé à blender à 60 fps
        self.msg = osc.Message("/all_OSC_data")
        for key, value in self.pool.items():
            self.msg.add(key[0])
            for i in range(2):
                for item in value[i]: # value = [ [0, 0, 0] , [0, 0] ]
                    self.msg.add(item)
        return self.msg

    def reset_data(self):
        self.pool = {}
        self.ACTA = {}
        print "Reset pool and ACTA ..."

# only to test
if __name__ == "__main__":
    # set instance of class
    game = allOscData()
