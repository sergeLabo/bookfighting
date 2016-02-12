## config.py

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

from bge import logic as gl

''' Ce script est le seul script oÃ¹ vous pouvez changez des variables '''

def main():
    # Le script externe ne doit ètre lancé qu'une seule fois mème avec retour au menu
    gl.one_script = False

    # Config du réseau
    gl.port_out = 8080 # Pour envoyer des datas aux téléphones
    gl.port_in = 8000  # Pour recevoir les datas du script server.py

    print("Début du jeu")
