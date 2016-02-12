## refereeing.py

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
Class qui gère les scores, jeux, sets, gagnants, perdants, annonce du score,  ...

TODO: this is a draft

"""

import os, signal
from random import choice
import bge
from bge import logic as gl

class Refereeing():
    def __init__(self):
        pass

    def run(self):
        winner()
        J_key()
        commentaire()
        annonce_score()
        if gl.cube['quit'] == 1:
            jeu_set_et_match()

def winner():
    a = 0
    for player in gl.activ_player:
        if gl.bookOPY[player].nbLivre != 0:
            a = 1
    if a == 0:
        jeu_update()
        for player in gl.activ_player:
            gl.bookOPY[player].get_5_books()

def J_key():
    # Si touche J
    J_status = gl.keyboard.events[bge.events.JKEY]
    if J_status == gl.KX_INPUT_JUST_ACTIVATED:
        print("Fin du jeu")
        jeu_update()
        for player in gl.activ_player:
            gl.bookOPY[player].get_5_books()

def jeu_update():
    # falaise gagne: +1 jeu
    if gl.score[1] > gl.score[3]:
        gl.objScore[0]["score"] += 1
    # égalité: falaise et plaine gagne 1 jeu
    if gl.score[1] == gl.score[3]:
        gl.objScore[0]["score"] += 1
        gl.objScore[2]["score"] += 1
    # plaine gagne: +1 jeu
    if gl.score[1] < gl.score[3]:
        gl.objScore[2]["score"] += 1

    # RAZ des points
    gl.objScore[1]["score"] = 0
    gl.objScore[3]["score"] = 0

def commentaire():
    # Commentaire de l'arbitre au hasard toutes les 10 secondes
    if gl.tempo == 600:
        all_keys = list(gl.comment.keys())
        gl.comment[choice(all_keys)].play()

def jeu_set_et_match():
    '''Annonce 'falaise ou plaine: jeu set et match' si quit'''
    # Send quit message
    message = ('127.0.0.1', 9000), "/quit", 1
    gl.dataOutOPY.send_message(message)

    # Rythme pendant 3 secondes
    gl.rythm1 += 1
    if gl.rythm1 ==   1 :
        if gl.score[0] >= gl.score[2]:
            gl.annonce["falaise"].play()
        else:
            gl.annonce["plaine"].play()
    if gl.rythm1 ==  50:
        gl.annonce["jeu"].play()
    if gl.rythm1 == 90:
        gl.annonce["set"].play()
    if gl.rythm1 == 140:
        gl.annonce["etmatch"].play()
        server_terminate()

def server_terminate():
    # Fin du subprocessus
    pid = gl.server_subprocess.pid
    print("Début de la fin du jeu")
    print("Fin du processus avec PID =", pid)
    gl.server_subprocess.terminate()
    print("Fin de la fin du jeu")

def annonce_score():
    '''Lance l'annonce après chaque point'''
    # Pour les score dans le jeu de plaine ou falaise
    for a in [1, 3]:
        if gl.score[a] != gl.objScore[a]["score"] :
            gl.score[a] = gl.objScore[a]["score"]
            if gl.store_annonce[2] == 0:
                # La 3ème valeur à 1 lance l'annonce
                gl.store_annonce = [gl.objScore[1]["score"], gl.objScore[3]["score"], 1]
                # pas d'annonce 0 a 0
                if gl.objScore[1]["score"] == 0 and gl.objScore[3]["score"] == 0:
                    gl.store_annonce[2] = 0

    # annonce en cours
    if gl.store_annonce[2] == 1:
        gl.rythm += 1
        if gl.rythm == 1 :
            gl.annonce[str(gl.objScore[1]["score"])].play(0.3)
        if gl.rythm == 20:
            gl.annonce["a"].play(0.3)
        if gl.rythm == 30:
            gl.annonce[str(gl.objScore[3]["score"])].play(0.3)
        if gl.rythm > 50:
            gl.store_annonce[2] = 0
            gl.rythm = 0
