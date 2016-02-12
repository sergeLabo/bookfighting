## initGame.py

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
    Ces variables sont utilisées dans  les scripts et sont des variables globales.
    Ce script ne tourne qu'une seule fois au début de la scène Game. '''

from bge import logic as gl

def main():
    init_variabe()
    get_object()

def init_variabe():
    set_mouvement_auto()
    gl.init_bf = False
    gl.accz_average = [[0, 9.8], [0, 9.8], [0, 9.8], [0, 9.8]]
    gl.iphone = [1,1,1,1]
    gl.probleme = ""
    gl.rythm = 0
    gl.rythm1 = 0
    gl.score = [0,0,0,0]
    gl.store_annonce = [0,0,0]
    # Remise à 0 du browser si retour à Menu depuis Game
    gl.browser = 0

def set_mouvement_auto():
    '''
    Vleurs intitiales pour calcul de position des joueurs autos
    A = point proche de 0 sur x, A varie de 0 à 0.4
    B = point proche de 1 sur x, B varie de 0.6 à 1
    C = point proche de 0 sur y, C varie de 0 à 0.4
    D = point proche de 1 sur y, D varie de 0.6 à 1
    E = point proche de 7 sur z, E varie de 7 à 15
    Z = point haut du saut sur z, Z varie de 9 à 15
    pente = vitesse du déplacement, varie de acc_min à acc_sup
    penteZ varie de 0 à 0.2
    acc_min et acc_sup = plage de variation des acc, varie de 1 à 15 /1000

    random is not random, les valeurs initiales des mouvements automatiques de
    chaque joueur doivent ètre différentes sinon ils font tous la mème chose

    gl.mvt_auto = [[X, penteX, A, B, Y, penteY, C, D, Z, penteZ, E],

            [ X,  penteX, A,   B,   Y,   penteY, C,   D,    Z, penteZ,  E] '''
    a = [   [ 0.1, 0.001, 0.1, 0.9, 0.3, 0.002,  0.2, 0.8,  9,  0.15,  15],
            [ 0.2, 0.002, 0.2, 0.8, 0.3, 0.003,  0.3, 0.8, 10,  0.16,  14],
            [ 0.3, 0.003, 0.3, 0.7, 0.3, 0.004,  0.4, 0.8, 11,  0.17,  13],
            [ 0.4, 0.004, 0.4, 0.6, 0.3, 0.005,  0.2, 0.8, 12,  0.18,  12]]
    gl.mvt_auto = []
    for i in a:
        gl.mvt_auto.append(i)

def get_object():
    # Liste des objects dans la scène
    scene = gl.getCurrentScene()
    objList = scene.objects

    # Le cube rose a beaucoup de briques et de propriétés
    gl.cube = objList["Cube"]
    # Le cube blanc est utilisé pour les joueurs autos et
    # le jeu à la souris et clavier
    gl.clavier = objList["clavier"]
    # La flèche
    gl.fleche = objList["fleche"]
    # Texte hurleur pour afficher des problèmes en gros
    gl.hurleur = objList["hurleur"]
    # Les 4 scores
    gl.objScore = []
    for i in range(4):
        gl.objScore.append(objList["score"+str(i)])
