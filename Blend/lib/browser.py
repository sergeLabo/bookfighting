## browser.py

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

''' Lancement d'un navigateur pour aller sur le blog '''

from bge import logic as gl
import webbrowser

def main():
    if gl.http["clic"] == 1:
        # On ne peut lancer qu'une seule fois sinon la durée du clic ouvre plusieurs navigateurs
        if gl.browser == 0:
            gl.browser = 1
            webbrowser.open_new("http://bookfighting.blogspot.fr/")

    # Affichage de l'ip dans le menu configuration
    gl.objIP["Text"] = gl.local_ip
