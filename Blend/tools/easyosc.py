## easyosc.py

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

''' Class utilisable pour:
- récupérer et traiter des messages OSC
- envoyer des messages OSC
- le seul script OSC python3 est le bon vieux OSC.py actualisé en python3'''

from time import sleep
import socket
try:
    # Import depuis le blend avec les script dans lib et OSC.py dans OSC3
    from .OSC3.OSC import decodeOSC, OSCClient, OSCMessage
except:
    # Import pour test du script ici
    from OSC3.OSC import decodeOSC, OSCClient, OSCMessage


class GetOsc():
    ''' Récupère les datas OSC, décode, met à jour un dictionnaire '''
    def __init__(self, ip="127.0.0.1", port=8000, buffer_size=1024, timeout=0.01):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.receive_nbr = 0
        self.failed = 0
        self.ratio = 1

    def ratio_reception(self):
        # Calcul du ratio de réception, le socket ne récupère pas toujours des datas à chaque frame
        self.ratio = (self.receive_nbr - self.failed)/self.receive_nbr
        self.failed = 0
        self.receive_nbr = 0
        print('Ratio de réception dans get_osc.py= {0:.2f}'.format(self.ratio))

    def connexion(self):
        # Création d'un socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.ip, self.port))
            self.sock.setblocking(0)
            self.sock.settimeout(self.timeout)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size)
            print("Réception des datas OSC sur :")
            print("IP = {} : Port = {}  avec un Buffer = {}".format(self.ip, self.port, self.buffer_size))
            print()
        except:
            print("Pas de connexion sur IP={} Port={}".format(self.ip, self.port))

    def receive(self):
        data = []
        try:
            self.receive_nbr += 1
            raw_data = self.sock.recv(self.buffer_size)
            data = decodeOSC(raw_data)
            #print("data =", data)
        except socket.error:
            self.failed += 1
            pass
            print("Pas de reception dans la fonction receive() de GetOSC")
        if self.receive_nbr == 120:
            self.ratio_reception()
        return data


class SendOsc(OSCClient):
    ''' Envoi d'un message '''

    def __init__(self):
        # Création de la connexion
        OSCClient.__init__(self, server=None)

    def send_message(self, address, title, message):
        # Création du message OSC
        msg = OSCMessage(title)
        msg.append(message)
        # Envoi
        try:
            OSCClient.sendto(self, msg, address)
            #print("Envoi de :", title, message, address)
        except:
            print("Problème lors de l'envoi à l'adresse {}".format(address))


if __name__ == "__main__":
    # Only to test
    # à tester avec le patch puredata joint dans le dossier
    getOPY = GetOsc("192.168.1.4", 9000, 1024)
    getOPY.connexion()
    sendOPY = SendOsc()

    a = 0
    while True:
        sleep(0.15)
        data = getOPY.receive()
        ##a += 0.15
        ##sendOPY.send_message(('127.0.0.1', 9000), "/blender/x", -15 + a)
        print(data)
        ##try:
            ##if data[0] == "/acc":
                ##print(data)
        ##except:
            ##pass
