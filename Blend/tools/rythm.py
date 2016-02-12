## rythm.py

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
Class générique qui permet de créer des événements avec un certain rythme

fait = Rythm(depart, fait, ceci, cela)
fait.do()

Top départ
 à t1 plus tard --> fait ceci
 à t2 plus tard --> fait cela
 etc ...

"""

class Rythm():
    def __init__(self, *args):
        self.args = args

    def do(self):
        pass
