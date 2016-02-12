## player.py

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
Class qui définit l'objet player créé et maj dans bookfighting.py
'''


from random import uniform
from bge import logic as gl
from mathutils import Euler

class Player():
    '''
    Un joueur est un objet dans Blender qui s'appelle p1, p2, p3, p4
    player = entier de 0 à 3
    self.data = data du joueur clavier ou auto ou phone
    self.stack = pile de 10 self.data
    '''
    def __init__(self, player):
        self.player = player
        self.data = []
        self.stack = []
        self.tonus = 1
        self.message = []

    def get_playerOPY(self):
        # Liste des objects dans la scène
        scene = gl.getCurrentScene()
        objList = scene.objects
        # l'objet dans Blender
        self.p = objList["p"+str(self.player)]
        # ombre
        self.o = objList["ombreDanseur"+str(self.player)]
        # La main
        self.h = objList["hand"+str(self.player)]
        return self.p, self.o, self.h

    def player_position(self):
        # Le joueur se déplace en fonction de x, y et accz, k = coeff scene
        ## X
        X = self.data[4]
        # Set a and b in y = ax +b for each player
        a_b_X = [(15, -21), (15, 6), (-15, -6), (-15, 21)]
        # Use a and b
        # ax multiplié par 2 et b décalé de 5
        x = a_b_X[self.player][0] * X + a_b_X[self.player][1]
        m = 0
        k = 1
        if gl.original == 1:
            m = 25
            k = 2
        x = k * x + m

        ## Y
        Y = self.data[5]
        if Y < 0.3 : # avance vite
            a_b_Y = [(40, -36), (40, -36), (-40, 36), (-40, 36)]
        # avance plus faible pour éviter un conflit avec le jet du livre
        if 0.3 <= Y <= 0.7 :
            a_b_Y = [(20, -30), (20, -30), (-20, 30), (-20, 30)]
        # il n'avance plus
        if Y > 0.7 :
            a_b_Y = [(0, -16), (0, -16), (0, 16), (0, 16)]
        # Use a and b
        y = a_b_Y[self.player][0] * Y + a_b_Y[self.player][1]

        ## Z
        Z = self.data[3]
        # Les capteurs de Z des téléphones ont une valeur moyenne qui diffère
        # d'un téléphone à l'autre
        accz = gl.accz_average[self.player][1]
        # the player is on earth if z = 7.6
        z = Z - accz + 7.4
        # Pour rester sur terre
        if z < 7.4:
            z = 7.4
        x, y , z = original_position(self.player, x, y , z, gl)
        return x, y , z

    def hand_rotation(self):
        # Définit la rotation avec le dernier y
        y = self.data[5]
        if y > 0.75:
            y = 0.75

        if self.player in [0, 1]:
            alpha = -2*y - 3 # radians ?
        if self.player in [2, 3]: # inversion du sens
            alpha = 2*y - 1 # radians ?
        return alpha

    def data_attribution(self):
        ''' t = table d'attributuion des datas aux joueurs
            C = joueur au clavier souris
            A = joueur automatique
            n = joueur au téléphone = sa place dans la liste gl.data_phone
        '''
        p = self.player
        # Combien de joueur au téléphone
        try:
            gl.data_phone
        except:
            gl.data_phone = [] # si pas de data reçue
        phone = len(gl.data_phone)

        if gl.original == 0:
            # t = [   ["C", "C", "C", "C", 0],
            # t = [   ["A", "A", "A", "A", 0],
            t = [   ["C", "A",  0,  "A", 0],
                    ["A", "A", "A",  0,  1],
                    ["A",  0,   1,   1,  2],
                    ["A", "A", "A",  2,  3]   ]
        if gl.original == 1:
            t = [   ["C",  0 ,  1, "A",  3],
                    ["A", "A",  0,   0,  0],
                    ["A", "A",  1,   1,  1],
                    ["A", "A", "A",  2,  2]   ]

        gl.fleche.setVisible(False)
        if t[p][phone] == "C":
            # clavier
            self.data = joueur_clavier(gl)
            if gl.original == 0:
                self.tonus = 1
            else:
                self.tonus = 1
            # Ajout de la flèche
            gl.fleche.setVisible(True)

        if t[p][phone] == "A":
            # auto
            self.data = joueur_auto(gl, p)
            if gl.original == 0:
                self.tonus = 10
            else:
                self.tonus = 20

        if isinstance(t[p][phone], int):
            # t[p][phone] = numéro du joueur au phone avec la table
            qui = t[p][phone]
            self.data = joueur_phone(gl, qui)
            if gl.original == 0:
                self.tonus = 2
            else:
                self.tonus = 2

        self.stack = stack_update(self.stack, self.data, 10)

def original_position(player, x, y , z, gl):
    if gl.original:
        if player in [1, 3]:
            x = 0
            y = 0
            z = -10 - 10*player
    return x, y , z

def joueur_clavier(gl):
    '''Un joueur joue au clavier et avec la souris
    Avec la souris:
    Haut bas pour avancer reculer donc y
    Gauche droite pour le déplacement latéral donc x
    Molette pour régler l'élévation du tir
    Q pour sauter
    Espace pour ajouter un livre donc accx
    Le joueur au clavier est toujours le 0
    Si clavier, ajout de la flèche de tir
    '''
    # Récupération des entrées clavier et de la position de la souris
    # Space donne accx = -6
    accx = gl.clavier["accx"]
    # Repasse à 0
    gl.clavier["accx"] = 0
    # Saut
    accz = gl.clavier["accz"]
    # Souris
    x = gl.mouse_x
    y = gl.mouse_y
    accy = 2 - gl.clavier["wheel"]

    # Définir la direction de la flèche
    alpha = 0.3 + accy/9 # élévation
    beta = 0
    gamma = 0 # direction mais définit par x, y

    # set objects orientation with alpha, beta, gamma in degrees
    rot_en_euler = Euler([alpha, beta, gamma])

    # Orientation de la flèche
    gl.fleche.worldOrientation = rot_en_euler.to_matrix()

    data = ["clavier", accx, accy, accz, x, y]
    return data

def joueur_auto(gl, player):
    ''' Mise en forme de data pour simuler des joueurs autos qui bougent si le
    nombre de joueurs est inférieur à 4.

    Le joueur au clavier est compté mais les autos ne sont pas encore ajoutés
    A = point proche de 0 sur x, A varie de 0 à 0.2
    B = point proche de 1 sur x, B varie de 0.8 à 1

    C = point proche de 0 sur y, C varie de 0 à 0.3
    D = point proche de 1 sur y, D varie de 0.7 à 1

    E = point haut sur z, E varie de 0 à 15
    Point bas du saut sur z = -6, les valeurs < 7 sont tronquées pour donner
    une vitesse initiale et finale forte, ça aussi créer des aléas dans le saut

    pente = vitesse du déplacement, varie de acc_min à acc_sup
    penteZ varie de 0 à 0.2
    acc_min et acc_sup = plage de variation des acc, varie de 1 à 15 /1000

    gl.mvt_auto = [[X, penteX, A, B, Y, penteY, C, D, Z, penteZ, E], etc
    '''
    # Récupération des valeurs de la frame précédente
    X = gl.mvt_auto[player][0]
    penteX = gl.mvt_auto[player][1]
    A = gl.mvt_auto[player][2]
    B = gl.mvt_auto[player][3]

    Y = gl.mvt_auto[player][4]
    penteY = gl.mvt_auto[player][5]
    C = gl.mvt_auto[player][6]
    D = gl.mvt_auto[player][7]

    Z = gl.mvt_auto[player][8]
    penteZ = gl.mvt_auto[player][9]
    E = gl.mvt_auto[player][10]

    # Plage d'accélération en fonction du score
    acc_min, acc_sup = get_variation(gl.objScore[0]["score"])

    # calcul des nouvelles valeurs
    X = fictive_pos_X(gl, player, X, penteX, A, B, acc_min, acc_sup)
    Y = fictive_pos_Y(gl, player, Y, penteY, C, D, acc_min, acc_sup)
    Z = fictive_pos_Z(gl, player, Z, penteZ, E)

    #           id                  accx          accy accz x  y
    data = ["auto"+str(player), uniform(-6, 0), 0,    Z,  X, Y]
    return data

def joueur_phone(gl, qui):
    data = gl.data_phone[qui]
    return data

def get_variation(score):
    ''' Variation des vitesses des mouvements autos avec le score des jeux de
    falaise, acc_min et acc_sup = plage de variation des acc '''
    variation = {   0: (1, 3),
                    1: (2, 5),
                    2: (3, 7),
                    3: (4, 9),
                    4: (5, 11),
                    5: (6, 13),
                    6: (7, 15)  }
    if score <= 6:
        acc_min, acc_sup = variation[score]
    else:
        acc_min, acc_sup = variation[6]
    return acc_min/1000, acc_sup/1000

def fictive_pos_X(gl, player, X, penteX, A, B, acc_min, acc_sup):
    # Ajout de penteX pour déplacement de penteX
    X += penteX
    # Sauvegarde
    gl.mvt_auto[player][0] = X

    # Si le joueur arrive en A,
    # on recalcule une nouvelle butée B et une nouvelle vitesse
    if X <= A :
        penteX = uniform(acc_min, acc_sup)
        B = uniform(0.95, 1.0) # grande plage de la course
        # Sauvegarde
        gl.mvt_auto[player][0] = A
        gl.mvt_auto[player][1] = penteX
        gl.mvt_auto[player][3] = B
    # Si le joueur arrive en B,
    # on recalcule une nouvelle butée A et une nouvelle vitesse
    if X >= B:
        penteX = - uniform(acc_min, acc_sup)
        A = uniform(0.0, 0.05) # grande plage de la course
        # Sauvegarde
        gl.mvt_auto[player][0] = B
        gl.mvt_auto[player][1] = penteX
        gl.mvt_auto[player][2] = A
    # debug
    #X = 0.5
    return X

def fictive_pos_Y(gl, player, Y, penteY, C, D, acc_min, acc_sup):
    # Ajout de penteY pour déplacement de penteY
    Y += penteY
    # Sauvegarde
    gl.mvt_auto[player][4] = Y

    # Si le joueur arrive en C,
    # on recalcule une nouvelle butée D et une nouvelle vitesse
    if Y <= C:
        penteY = uniform(2*acc_min, 2*acc_sup)
        D = uniform(0.8, 1) # proche de 1 pour créer du mouvement
        # Sauvegarde
        gl.mvt_auto[player][4] = C
        gl.mvt_auto[player][5] = penteY
        gl.mvt_auto[player][7] = D
    # Si le joueur arrive en D,
    # on recalcule une nouvelle butée C et une nouvelle vitesse
    if Y >= D:
        penteY = - uniform(2*acc_min, 2*acc_sup)
        C = uniform(0.0, 0.2) # entre 0 et 0.2  pour récupération d' un livre
        # Sauvegarde
        gl.mvt_auto[player][4] = D
        gl.mvt_auto[player][5] = penteY
        gl.mvt_auto[player][6] = C
    # debug
    #Y = 0.5
    return Y

def fictive_pos_Z(gl, player, Z, penteZ, E):
    # Ajout de penteZ pour déplacement de penteZ
    Z += penteZ
    # Sauvegarde
    gl.mvt_auto[player][8] = Z

    # le joueur retombe
    # -2.0 est le point bas
    if Z < -6.0:
        penteZ = uniform(0.3, 0.9)
        # le joueur ne peut pas s'enfonçer dans le sol,
        #les valeurs inférieures à 7.4 ne donneront pas de mouvement,
        # pas de saut, ce qui donne une vitesse initiale forte
        E = uniform(-6.0, 15.0)
        Z = -6.0
        # Sauvegarde
        gl.mvt_auto[player][8] = Z
        gl.mvt_auto[player][9] = penteZ
        gl.mvt_auto[player][10] = E
    # le joueur est arrivé en haut, il retombe, mème vitesse que pour la montée
    if Z > E:
        penteZ = - penteZ
        # Sauvegarde
        gl.mvt_auto[player][8] = Z
        gl.mvt_auto[player][9] = penteZ
        gl.mvt_auto[player][10] = E
    return Z

def stack_update(pile, new_item, nb):
    ''' pile = la pile est une liste de longuer nb
        new_item = la valeur à ajouter
        nb = nombre d'item dans la pile
        la pile est tronquée si elle est trop longue
        new_item est répété si la pile est trop courte
    '''
    # Vérification des paramètres
    if not isinstance(pile, list):
        pile = []
    if not isinstance(nb, int):
        nb = 2
    if new_item == None:
        new_item = 0

    # Bourrage dans la pile si besoin
    if len(pile) < nb:
        while len(pile) < nb:
            pile.append(new_item)
    # Pile ok
    elif len(pile) == nb:
        # Ajout à la pile
        pile.append(new_item)
        # Suppression du premier
        del pile[0]
    # Pile trop longue
    elif len(pile) > nb:
        a = len(pile) - nb
        pile = pile[a:]
        # Ajout à la pile
        pile.append(new_item)
        # Suppression du premier
        del pile[0]

    return pile
