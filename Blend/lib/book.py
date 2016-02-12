## book.py

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
Class qui définit l'objet book créé et maj dans bookfighting.py

Convention:
trucOPY = objet python truc
trucOBL = objet Blender truc
    Les dernières datas du joueur:
    gl.playerOPY[player].data  = [accx, accy, accz, x, y]

    La pile avec les 10 dernières valeurs:
    gl.playerOPY[player].stack = [[accx, accy, accz, x, y]*10]

    Dans class Player()
    self.data  = [ip, accx, accy, accz, x, y]
    self.stack = [self.data*10]

"""

from bge import logic as gl

class Book():
    def __init__(self, player):
        self.player = player
        self.nbLivre = 5
        self.etatLivre = 5

    def get_bookOPY(self):
        # Liste des objects dans la scène
        scene = gl.getCurrentScene()
        objList = scene.objects
        # les 3 livres du joueur, une liste de 3
        self.b = [0,0,0]
        for j in range(3):
            self.b[j] = objList["book"+str(self.player)+str(j)]
        # Le livre de simulation du joueur
        self.bs = objList["book_simul"+str(self.player)]
        return self.b, self.bs

    def book_compteur(self):
        ''' 5 livres au départ, un livre jeté est décompté. Après le jet,
        le joueurobtient un livre si le téléphone est tourné. Récupération de
        5 livres quand tous les joueurs ont jeté tous leurs livres.
        avec
        self.nbLivre  = nombre le livres restant
        self.etatLivre = état du livre en cours
            si livre prèt à ètre lancé = 1
            si livre vient d'ètre lancé = 2
            ajout fait mais en attente de y proche de zéro = 3
            y proche de zéroajout fait mais en attente de ajout = 4
            valeur initiale qui bloque = 5
        '''
        p = self.player
        y     = gl.playerOPY[p].data[5]
        accx  = gl.playerOPY[p].data[1]

        # Déblocage initial
        if self.etatLivre == 5 and y < 0.2:
            self.etatLivre = 1

        # Le livre vient d'ètre lancé, le téléphone est tourné, puis y en bas
        if self.etatLivre == 2 and accx < -5.0:
            self.etatLivre = 3
        if self.etatLivre == 3 and y < 0.2 and self.nbLivre > 0:
            self.etatLivre = 1

        # Le livre vient d'ètre lancé, y en bas puis le téléphone est tourné
        if self.etatLivre == 2 and y < 0.2:
            self.etatLivre = 4
        if self.etatLivre == 4 and accx*gl.iphone[p] < -5.0 and self.nbLivre > 0:
            self.etatLivre = 1

    def book_change(self):
        # le livre s'ouvre pendant le vol
        # book(i)0 est remplacé par book(i)1 puis par book(i)2
        p = self.player
        book = gl.bookOBL[p][0]
        str_p = str(p)
        # Vu depuis les cases
        if p in [0,1]:
            # Si le livre passe le 1er tiers
            if book.worldPosition[1] > -10:
                book.replaceMesh('book' + str_p + '1')
            else:
                book.replaceMesh('book' + str_p + '0')
            # Si le livre passe le second tiers
            if book.worldPosition[1] > 10:
                book.replaceMesh('book' + str_p + '2')

        if p in [2,3]:
            # Si le livre passe le second tiers
            if book.worldPosition[1] < 10:
                book.replaceMesh('book' + str_p + '1')
            else:
                book.replaceMesh('book' + str_p + '0')
            # Si le livre passe le 1er tiers
            if book.worldPosition[1] < -10:
                book.replaceMesh('book' + str_p + '2')

    def book_dans_main(self):
        p = self.player
        y = gl.playerOPY[p].data[5]
        if y < 0.8 and self.etatLivre == 1:
            # Le livre est dans la main, à la place de book_simul
            # Récup des objets Blender
            book = gl.bookOBL[p] # gl.bookOBL liste de 4
            bookSimul = gl.bookSimOBL[p] # idem

            # Disable Dynamics: le livre est dans la main
            book[0].suspendDynamics()

            # Placement livre 0 à la plce de book simul qui est dans la main
            book[0].worldPosition    = bookSimul.worldPosition
            book[0].worldOrientation = bookSimul.worldOrientation

    def book_lance(self):
        # le livre est prèt à ètre lancé
        p = self.player
        book = gl.bookOBL[p][0]

        # Les plus anciennes et les dernières valeurs, liste de 10
        old = 0
        stack_old = gl.playerOPY[p].stack[old]
        stack_new = gl.playerOPY[p].stack[9]
        # Le dernier y
        y = stack_new[5]
        # pour vz avec inclinaison accy , accy varie de -10 à 10
        accy = stack_new[2]

        if y > 0.8 and self.etatLivre == 1:
            # Restauration de Dynamics pour voler
            book.restoreDynamics()

            # Delta t pour l'intégration
            dT = 0.075
            # Formule: vx = ( x(n) - x(n-10) ) /dT
            vx = ( stack_new[4] - stack_old[4] )/dT
            vy = ( stack_new[5] - stack_old[5] )/dT
            # En fonction du coté
            if p in [0, 1]:
                vx = 3 * vx
                vy = 6 * vy
            if p in [2, 3]:
                vx = -3 * vx
                vy = -6 * vy
            vz = 1 * accy # accy de -10 à 10

            # Jouabilité ajustée en fonction de old et scene avec tonus
            tonus = gl.playerOPY[p].tonus
            vx = tonus * vx
            vy = tonus * vy
            vz = tonus * vz
            if p == 0:
                print("Vitesse de mon livre =", (vx**2+vy**2+vz**2)**0.5, "vx =", vx, "vy =", vy, "vz =", vz)

            # # Application de la vitesse initiale
            book.worldLinearVelocity = [vx, vy, vz]

            # Le livre vient d'ètre lancé
            self.etatLivre = 2
            self.nbLivre -= 1
            # Lancement du son du livre lancé
            gl.sound["livre"].play()

    def get_5_books(self):
        self.etatLivre = 5
        self.nbLivre = 5

    def create_messages_TouchOSC(self):
        ''' Create a list with the 5 toggles state to send to phone
                                (ip, port)  title    message
        messages = [[(ip, 9001),'/4/toogle1',1], [(ip, 9001),'/4/toogle2',0], [(ip, 9001), '/4/toogle3',0], etc]'''
        ip = gl.playerOPY[self.player].stack[0][0]
        messages = []
        if "auto" in ip:
            messages = []
        elif "clavier" in ip:
            messages = []
        else:
            # Pour les 5 toggles
            for i in range(5):
                if i < gl.bookOPY[self.player].nbLivre:
                    j = 1
                else:
                    j = 0
                messages.append(((ip, gl.port_out), '/4/toggle'+str(i+1), j))
        return messages

    def create_messages_ControlOSC(self):
        ''' Create a list with the 5 toggles state to send to phone
                                (ip, port)  title    message
        messages = [[(ip, 9001),'/bouton1',1], [(ip, 9001),'/buttons/2',0], [(ip, 9001), '/buttons/3',0], etc]'''
        ip = gl.playerOPY[self.player].stack[0][0]
        messages = []
        if "auto" in ip:
            messages = []
        elif "clavier" in ip:
            messages = []
        else:
            # Pour les 5 toggles
            for i in range(5):
                # j = Etat du button
                if i < gl.bookOPY[self.player].nbLivre:
                    j = 1
                else:
                    j = 0
                messages.append(((ip, 8080), '/boutons'+str(i+1), j))
        return messages
