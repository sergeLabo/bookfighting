## init_menu.py

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

''' Initialisation des variables comme attributs du GameLogic.
    Ces variables sont utilisées dans  les scripts et sont des variables
    globales. Tue les processus de scripts existants.
    Ce script ne tourne qu'une seule fois au début de la scène Menu. '''

import subprocess
import sys
from os import system
from bge import logic as gl
from time import sleep, time
from tools.sometools import get_my_ip

def main():
    if not gl.one_script:
        print("\n Initialisation du jeu: \n")
        init_variable()
        get_object()
        gl.local_ip = get_my_ip()
        kill_python_processus()
        sleep(1)
        run_local_server()
        gl.one_script = True
    else:
        print("Retour au menu avec reset()")
        get_object()
        reset_variable() # pas propre

def reset_variable():
    ''' Si retour au menu principal, les variables et objects attributs du GameLogic sont conservés.
        Ceci est source de bug si il manque des reset'''
    gl.dataInOPY = None
    gl.dataOutOPY = None
    gl.displayOPY = None
    gl.textureDanseur2 = None
    gl.original = 0
    gl.activ_player = [0, 1, 2, 3]
    gl.iphone = [1,1,1,1]
    try:
        gl.music["bf2"].stop()
        print("Fin du bruit de fond: bf2.ogg")
    except:
        print("Pas de bruit de fond: bf2.ogg dans reset_variable() de initMenu.py")

def kill_python_processus():
    ''' Du code brutal si ça bug: les processus du serveur des instances précédentes du jeu sont tués'''
    try:
        print("Kill de tous les processus python2.7")
        system('killall -9  python2.7')
        print("Kill réussi")
    except:
        print("Pas de script python2.7 en cours")

def init_variable():
    ## Init des variables
    # Temps zéro pour affichage du temps depuis lancement du jeu
    gl.t0 = time()
    # On ne peut lancer qu'une seule fois sinon la durée du clic ouvre plusieurs navigateurs
    gl.browser = 0

def run_local_server():
    ## Lancement du script server externe à Blender
    # Chemin vers le script
    path = sys.path[0]
    script = path + "/Server/server.py"
    # Excécution du script
    gl.server_subprocess = subprocess.Popen(['python2.7 ' + script +';read'],
                            stdout= subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
    print("PID du script qui reçoit les datas des TouchOSC = ", gl.server_subprocess.pid, "\n")

def get_object():
    # Liste des objects dans la scène
    scene = gl.getCurrentScene()
    print ("Initialisation de la scène Menu: Liste des scènes =", scene)
    objList = scene.objects

    # le plan avec http du 1er menu
    gl.http = objList["http"]

    # le Text pour ip
    gl.objIP = objList["ip"]
