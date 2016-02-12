## data.py

#############################################################################
# Copyright (C) SergeBlender April 2013
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

"""
Class qui définit l'objet data créé et maj dans bookfighting.py

Convention:
trucOPY = objet python truc
trucOBL = objet Blender truc

Ce script reçoit et envoie en OSC, met en forme les datas.
Chaque objet joueur crée dans bookfighting.py a un attribut data
avec ses propres datas.

data d'un joueur = [ip, accx, accy, accz, x, y]

Utilisation:
gl.dataInOPY = DataIn(gl)
gl.playerOPY[player].data = gl.dataInOPY.update(gl)
accx = gl.playerOPY[player].data[1]
y    = gl.playerOPY[player].data[5]

"""

from bge import logic as gl
from tools.easyosc import GetOsc, SendOsc

class DataIn():
    def __init__(self, ip, port, buffer_size, timeout):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        # Get OSC
        self.receiveOPY = GetOsc(ip, port, buffer_size, timeout)
        self.receiveOPY.connexion()

    def dataIn(self):
        ''' gl.data_phone = [[phone1], [phone2]]
            avec phone1 = [ip, accx, accy, accz, x, y]
        '''
        # Reception des datas à mettre en forme
        data = self.receiveOPY.receive()
        # Mise en forme et attribution
        data_phone = set_data_in_list(data)
        return data_phone


class DataOut():
    def __init__(self):
        # Send OSC
        self.sendOPY = SendOsc()

    def send_list(self, messages):
        ''' messages = [[('127.0.0.1', 9001), "/x", -15)], [], ...]'''
        if messages:
            for m in messages:
                self.sendOPY.send_message((m[0][0], m[0][1]), m[1], m[2])
        #print("Messages envoyés au téléphones: ", messages)

    def send_message(self, m):
        ''' messages = ('127.0.0.1', 9000), "/quit", 1 '''
        self.sendOPY.send_message((m[0][0], m[0][1]), m[1], m[2])


def set_data_in_list(data):
    if '/all_OSC_data' in data:
        # Je coupe '/all_OSC_data', ',sfffff'
        data = data[2:]
        # Combien de data par joueur
        num_item = 6
        # Je divise la longue liste en liste de liste par joueur
        # data = [data du joueur 1, data du joueur 2]
        # avec data du joueur 1 = [ip, accx, accy, accz, x,y]
        data = chunks(data, num_item)
        # Maxi 4 joueurs au cas oÃ¹
        data = data[:4]
    else:
        data = []
    return data

def chunks(list_to_cut, num_item):
    ''' Découpage d'une liste en liste de longueur n,
        la liste doit donc avoir une longeur multiple de n. '''
    if len(list_to_cut) % num_item == 0 :
        return [list_to_cut[i:i+num_item] for i in range(0, len(list_to_cut), num_item)]
    else:
        list_to_cut = []
        print("La liste", list_to_cut, "n'est pas un multiple de", num_item)
