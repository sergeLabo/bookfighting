## bookfighting.py

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

""" Gestion du jeu BookFighting

Convention:
trucOPY = objet python truc
trucOBL = objet Blender truc

Création des objets python et Blender , tout est attribut du GameLogic=gl
    Example: Objets python
        gl.playerOPY
        gl.bookOPY
        gl.dataInOPY

    Example: Objets dans Blender
        gl.playerOBL
        gl.ombreOBL
        gl.bookOBL
        gl.bookSimOBL

Ce script tourne à chaque frame dans la scène Game et dans la scène Original
"""

import os,sys
from time import time, sleep
from pprint import pprint

from bge import logic as gl
# Ajotut de chemin pour être sûr que les tools et lib seront trouvés sur debian et win$
sys.path.append(gl.expandPath('//tools'))
sys.path.append(gl.expandPath('//lib'))
print("Répertoires des bibliothèques python =", sys.path)

from bge import texture
from tools.sometools import print_str_args
from lib.player import Player
from lib.book import Book
from lib.data import DataIn, DataOut
from lib.display import Display
from lib.refereeing import Refereeing
from tools.textureChange import TextureChange
from tools.sound import EasyAudio
from tools.tempo import Tempo

def main():
    # Une seule fois
    if not gl.init_bf:
        init_Game_or_Original_scene()
        gl.init_bf = True

    # Ensuite, exécuté à chaque frame
    if gl.init_bf:
        tempo()
        gamePlay()
        print_some()

def init_Game_or_Original_scene():
    # Exécuté une seule fois
    init_tempo()
    init_objet()
    gl.dataInOPY = DataIn('localhost', gl.port_in, 1024, 0.01)
    gl.dataOutOPY = DataOut()
    gl.displayOPY = Display()
    init_audio()
    gl.music["bf2"].repeat()
    gl.refereeingOPY = Refereeing()
    # Active player
    gl.activ_player = [0, 1, 2, 3]
    # Init particulier pour la scène Original
    init_original_only()

def init_tempo():
    # Tempo pour le jeu de caméra de l'intro
    gl.tempo_introOPY = Tempo(400, 1)
    gl.tempo_intro = gl.tempo_introOPY.create()
    gl.tempo_introOPY.lock()

    # Création d'un autre object tempo de 10s
    gl.tempoOPY = Tempo(601, 1)
    gl.tempo = gl.tempoOPY.create()

    # Tempo utilisée pour le print toutes les 2s
    gl.tempo_globaleOPY = Tempo(121, 1)
    gl.tempo_globale = gl.tempo_globaleOPY.create()

    # Tempo pour animation personnage
    gl.tempo_persoOPY = Tempo(61, 1)
    gl.tempo_perso = gl.tempo_persoOPY.create()

    # Nous ne repasserons plus par ici
    gl.init_tempo = True

def init_objet():
    # joueur
    gl.playerOPY = [0,0,0,0]
    gl.playerOBL = [0,0,0,0]
    gl.ombreOBL = [0,0,0,0]
    gl.handOBL = [0,0,0,0]
    for i in range(4):
        # Je définis les objets python représentants les joueurs
        gl.playerOPY[i] = Player(i)
        # Je définis la liste des objets joueurs, ombre et hand dans blender
        (a, b, c) = gl.playerOPY[i].get_playerOPY()
        gl.playerOBL[i], gl.ombreOBL[i], gl.handOBL[i] = (a, b, c)

    # livre
    gl.bookOPY = [0,0,0,0]
    # Les livres d'un joueur est une liste de 3
    gl.bookOBL = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    gl.bookSimOBL = [0,0,0,0]
    for i in range(4):
        # Je définis les objets python représentants les livres
        gl.bookOPY[i] = Book(i)
        # Je définis la liste des objets livre dans blender,
        # les 3 livres du joueur et le livre de simulation
        gl.bookOBL[i], gl.bookSimOBL[i] = gl.bookOPY[i].get_bookOPY()

def init_audio():
    # son
    comment = [ "attentionDanger", "bienJouer", "bravo", "enPlaceSaluez", "magnifique",
                "mordu", "non", "rater", "toucherAh", "tropFort" ]
    music = ["bf1", "bf2"]
    annonce = [   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                "a", "jeu", "set", "etmatch", "falaise", "plaine"]
    sound = ["livre", "bruitFond"]

    # gl.sound est un dictionnaire: { "boum": fabrique de boum.ogg, ....}
    gl.comment = EasyAudio(comment, "//audio/comment/")
    gl.music = EasyAudio(music, "//audio/music/")
    gl.annonce = EasyAudio(annonce, "//audio/annonce/")
    gl.sound = EasyAudio(sound, "//audio/sound/")

def init_original_only():
    ''' Réglages pour la scène Original'''
    # Set si scène = Game
    gl.original = 0
    # Liste des objects dans la scène
    scene = gl.getCurrentScene()
    if scene.name == "Original":
        # Seuls les joueurs 0 et 2 sont activés, les autres sont placés loin à coté
        gl.activ_player = [0, 2]
        # seulement le joueur 0
        gl.playerOBL[0].setVisible(False)
        # tous les objets de 1 et 3
        for i in [1, 3]:
            liste = [gl.bookOBL[i][0], gl.ombreOBL[i], gl.playerOBL[i], gl.handOBL[i]]
            for obj in liste:
                obj.setVisible(False)

        sleep(5)
        # Changement de textures
        gl.textureDanseur2 = TextureChange(gl.playerOBL[2], "danseur2.png")
        gl.textureDanseur2.texture_new("//textures/perso.png")

        gl.textureOmbreDanseur2 = TextureChange(gl.ombreOBL[2], "danseur ombre.png")
        gl.textureOmbreDanseur2.texture_new("perso ombre.png")

        # Placement du panneau de score au fond
        objList = scene.objects
        info = objList["info"]
        info.localPosition = [-23, 36, 20]
        # On ne repasse plus par ici
        gl.original = 1

def anim_perso():
    # TODO: devrait ètre dans player.py
    if gl.tempo_perso == 20:
        gl.textureDanseur2.texture_new("perso1.png")
    if gl.tempo_perso == 40:
        gl.textureDanseur2.texture_new("perso2.png")
    if gl.tempo_perso == 60:
        gl.textureDanseur2.texture_new("perso.png")

def gamePlay():
    # Tourne à chaque frame
    # ---- Maj des datas ---- #
    gl.data_phone = gl.dataInOPY.dataIn()
    # ---- Maj affichage ---- #
    gl.displayOPY.update_view()
    # ---- Maj souris ---- #
    gl.displayOPY.mouse()
    # ---- Actions ---- #
    for player in gl.activ_player:
        each_player(player)
    # ---- Refereeing ---- #
    gl.refereeingOPY.run()

def each_player(player):
    # Get data and set attribut data to player
    gl.playerOPY[player].data_attribution()

    # position des joueurs
    x, y , z = gl.playerOPY[player].player_position()
    # j'applique les coordonnées
    gl.playerOBL[player].localPosition = [x , y, z]
    # idem avec l'ombre
    gl.ombreOBL[player].localPosition = [x , y, 0.36]
    # Rotation de la main
    alpha = gl.playerOPY[player].hand_rotation()
    gl.handOBL[player].worldOrientation = (alpha, 0, 0)
    ### Changement de textures
    ##if gl.original:
        ##anim_perso()

    # ---- Book ---- #
    accx1 = gl.playerOPY[player].data[1]
    y1    = gl.playerOPY[player].data[5]
    gl.bookOPY[player].book_compteur()
    gl.bookOPY[player].book_dans_main()
    gl.bookOPY[player].book_lance()
    gl.bookOPY[player].book_change()
    # Toutes les secondes, avec décalage pour chaque joueur
    if gl.tempo  % 60 == 0 + 10 * player:
        messages_TouchOSC = gl.bookOPY[player].create_messages_TouchOSC()
        messages_ControlOSC = gl.bookOPY[player].create_messages_ControlOSC()
        gl.dataOutOPY.send_list(messages_TouchOSC)
        gl.dataOutOPY.send_list(messages_ControlOSC)
        ### Je suis en vie
        ##message = ('127.0.0.1', 9000), "/I_am_running", 1
        ##gl.dataOutOPY.send_message(message)
    # ---- phone ---- #
    accz_average(player)

def tempo():
    # maj de toutes les tempos à chaque frame
    gl.tempo_intro = gl.tempo_introOPY.update()
    gl.tempo = gl.tempoOPY.update()
    gl.tempo_globale = gl.tempo_globaleOPY.update()
    gl.tempo_perso = gl.tempo_persoOPY.update()

def accz_average(player):
    ''' Chaque téléphone a une valeur moyenne particulière du capteur d'accélération
        gl.accz_average = [[0, 9.8], [0, 9.8], [0, 9.8], [0, 9.8]]
        Par joueur,  1er = nombre de passage dans cette fonction, 2ème = valeur moyenne ou par défault '''
    if gl.accz_average[player][0] < 100:
        gl.accz_average[player][0] += 1 # pour que la pile soit pleine de bonne valeur
    # Au bout de 100 frames, je devrais avoir 10 bonnes dermières valeurs
    if gl.accz_average[player][0] == 100:
        gl.accz_average[player][0] = 101 # avec 101 cette fonction ne fait plus rien
        somme = 0
        for acc in gl.playerOPY[player].stack:
            somme = somme + acc[2]
        average = somme/10
        # Si valeur absurde ou si iphone qui envoie acc entre -1 et 1
        if -1 < average < 1:
            gl.iphone[player] = 1
        if average < 3:
            average = 9.8

        gl.accz_average[player][1] = average
        print(gl.playerOPY[player].stack[0][0], ": Capteur d'accélération en z =", gl.accz_average[player][1])

def print_some():
    ''' Imprime dans le terminal toutes les 10 secondes pour déboguer'''
    if gl.tempo == 1:
        Suivi_du_jeu = int(time() - gl.t0)
        print
        print("Le jeu tourne depuis {} secondes".format(Suivi_du_jeu))
        print_str_args('gl.data_phone')
        #gl.PrintGLInfo()

def bruit_de_fond():
    gl.sound["bruitFond"].repeat()
