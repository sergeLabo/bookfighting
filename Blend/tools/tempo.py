## tempoBlender.py

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

'''
Class utilisable pour des tempo et compteur
'''

class Tempo():
    ''' Les tempos sont en fait des compteurs qui sont mis à jour à chaque frames de Blender.
        Le script tempoBlender.py appelle la fonction update de cette classe à chaque frame.
        Paramètres:
        période: la tempo est remise à zéro si periode atteind
        pas: incrément de la tempo, par défaut=1, aucun intérèt de changer le pas
        verrou: si verrou, pas d'incrémentation '''

    def __init__(self, periode=60, pas=1):
        self.periode = periode
        self.verrou = False
        self.pas = pas
        self.tempo = 0

    def create(self):
        # Création de la variable
        return self.tempo

    def lock(self):
        # Verrou, je bloque
        self.verrou = True

    def unlock(self):
        # Pas de verrou, je peux incrémenter
        self.verrou = False

    def reset(self):
        # Remise à zéro de la tempo
        self.tempo = 0

    def update(self):
        # J'incrémente si pas de verrou. Si verrou, je ne fais rien
        if not self.verrou:
            self.tempo += self.pas
            if self.tempo > self.periode +1:
                self.tempo = 0
        return self.tempo


if __name__ == "__main__":
    # Only to test
    from time import sleep

    def test1():
        tempo_init = False

        if not tempo_init:
            # Création des objets

            # tempo pour le jeu de caméra de l'intro
            tempo_introOPY = Tempo(400, 1)
            tempo_intro = tempo_introOPY.create()
            tempo_introOPY.lock()

            # Création d'un autre object tempo
            tempoOPY = Tempo(601, 1)
            tempo = tempoOPY.create()

            # tempo utilisée pour le print toutes les 2s
            tempo_globaleOPY = Tempo(121, 1)
            tempo_globale = tempo_globaleOPY.create()

            # calcul du ratio de réception
            frame_nbrOPY = Tempo(1001, 1)
            frame_nbr = frame_nbrOPY.create()

            # Nous ne repasserons plus par ici
            tempo_init = True

            print("init ok")

        while tempo_init:
            sleep(0.1)
            # maj
            tempo_intro = tempo_introOPY.update()
            tempo = tempoOPY.update()
            tempo_globale = tempo_globaleOPY.update()
            frame_nbr = frame_nbrOPY.update()
            print(tempo_intro, tempo, tempo_globale, frame_nbr)

    def test2():
        # le code dans la boucle while est le code du script tempoBlender.py !!!
        # trop fort !!!

        from sometools import VirtualGl

        # Création de gl virtuel
        gl = VirtualGl()
        print("gl =", gl)

        gl.init_tempo = False

        while True:
            # Simulation de la pulsation de Blender à 60 fps
            sleep(0.015)
            if not gl.init_tempo:
                # Création des objects

                # tempo pour le jeu de caméra de l'intro
                gl.tempo_introOPY = Tempo(400, 1)
                gl.tempo_intro = gl.tempo_introOPY.create()
                gl.tempo_introOPY.lock()

                # Création d'un autre object tempo
                gl.tempoOPY = Tempo(601, 1)
                gl.tempo = gl.tempoOPY.create()

                # tempo utilisée pour le print toutes les 10s
                gl.tempo_globaleOPY = Tempo(601, 1)
                gl.tempo_globale = gl.tempo_globaleOPY.create()

                # Nous ne repasserons plus par ici
                gl.init_tempo = True

            if gl.init_tempo:
                # maj de toutes les tempos à chaque frame
                gl.tempo_intro = gl.tempo_introOPY.update()
                gl.tempo = gl.tempoOPY.update()
                gl.tempo_globale = gl.tempo_globaleOPY.update()
                print(gl.tempo_intro, gl.tempo, gl.tempo_globale)

    # Run test1
    #test1()

    # Run test2
    test2()
