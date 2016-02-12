## display.py

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
Class qui défini l'affichage, utilisé dans bookfighting.py
Permet de créer:
    Intro = jeu de caméra
    Vue 2 caméras
    Vue 1 caméra

gl est le GameLogic, get with : from bge import logic as gl

"""

from bge import logic as gl
from bge import render as Rasterizer

class Display():
    def __init__(self):
        # Liste des objects dans la scène
        scene = gl.getCurrentScene()
        objList = scene.objects
        # Récupère les 10 caméras
        self.objCam = []
        for i in range(10):
            self.objCam.append(objList["cam"+str(i)])

    def update_view(self):
        ''' Je débloque gl.tempo_intro pour lancer l'intro, jusqu'à la fin de l'intro
        soit 350, puis je rebloque pour ne plus lancer l'intro à partir de 351'''
        if gl.tempo_intro < 350:
            gl.tempo_introOPY.unlock()

            # Caméra vers le world bleu pour laisser à blender le temps de charger les images
            # puis jeu de caméra
            table_Game =  { 1: 2, 100: 3, 140: 4, 180: 5, 220: 6, 260: 7 }
            table_Original =  { 1: 2, 180: 8 }

            # Vue intro
            if gl.original == 0:
                for key, cam in table_Game.items():
                    if gl.tempo_intro == key:
                        A,B,C,D,H,W = self.reset_view()
                        self.objCam[cam].setViewport( 0, 0, W, H)
                        self.objCam[cam].useViewport = True
            # Pas d'intro
            else:
                for key, cam in table_Original.items():
                    if gl.tempo_intro == key:
                        A,B,C,D,H,W = self.reset_view()
                        self.objCam[cam].setViewport( 0, 0, W, H)
                        self.objCam[cam].useViewport = True

        # Vue finale
        if gl.tempo_intro == 350:
            gl.tempo_introOPY.lock()
            A,B,C,D,H,W = self.reset_view()
            if gl.original == 0:
                self.view_split(A, B, C, D, H, W)
            else:
                self.view_full(H, W)

    def reset_view(self):
        ''' Retourne largeur hauteur des fenètres,
            désactive toutes les caméras '''
        H = Rasterizer.getWindowHeight()
        W = Rasterizer.getWindowWidth()
        A = int(W*2/3)
        B = int(H/2)
        C = int(H/4)
        D = int(H*3/4)

        # Désactivation des 10 caméras
        for cam in range(10):
            self.objCam[cam].useViewport = False

        return (A, B, C, D, H ,W)

    def view_full(self, H, W):
        # Vue 1 caméra
        self.objCam[8].setViewport( 0, 0, W, H)
        self.objCam[8].useViewport = True

    def view_split(self, A, B, C, D, H, W):
        # Vue 2 caméras
        self.objCam[0].setViewport( 0, 0, W, B)
        self.objCam[0].useViewport = True

        self.objCam[1].setViewport( 0, B, W, H)
        self.objCam[1].useViewport = True

    def mouse(self):
        gl.mouse_x = 2*gl.mouse.position[0]
        gl.mouse_y = 2 - 2*gl.mouse.position[1]

        if gl.mouse_x < 0:
            gl.mouse_x = 0
        if gl.mouse_y < 0:
            gl.mouse_y = 0
        if gl.mouse_x > 1:
            gl.mouse_x = 1
        if gl.mouse_y > 1:
            gl.mouse_y = 1
