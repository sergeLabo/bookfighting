## sometools.py

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

import inspect
import subprocess,re, socket
from functools import reduce


class VirtualGl():
    ''' Classe vide pour simuler
    from bge import logic as gl
    Dommage que ça ne serve pas à grand chose
    '''
    def __init__(self):
        pass


def get_my_ip():
    # Retourne l'adresse ip du pc sur le réseau local

    #A generator that returns stripped lines of output from "ip address show"
    iplines=(line.strip() for line in subprocess.getoutput("ip address show").split('\n'))
    #Turn that into a list of IPv4 and IPv6 address/mask strings
    addresses1=reduce(lambda a,v:a+v,(re.findall(r"inet ([\d.]+/\d+)",line)+re.findall(r"inet6 ([\:\da-f]+/\d+)",
                                                                                            line) for line in iplines))
    #Get a list of IPv4 addresses as (IPstring,subnetsize) tuples
    ipv4s=[(ip,int(subnet)) for ip,subnet in (addr.split('/') for addr in addresses1 if '.' in addr)]
    # my IP
    try:
        ip = ipv4s[1][0]
        print("IP =", ip)
    except:
        print("Cet ordinateur n'est pas connecté à un réseau !")
        ip = "127.0.0.1"
    return ip

def print_str_args(*args):
    ''' Imprime en terminal les variables en argument
        Les variables doivent ètre sous forme de string,
        par exemple
        print_str_args("a")
        imprime la variable a qui a une valeur 42
        a = 42
        '''
    for i in args:
        record=inspect.getouterframes(inspect.currentframe())[1]
        frame=record[0]
        val=eval(i,frame.f_globals,frame.f_locals)
        print('{0} = {1}'.format(i, val))

def droiteAffine(x1, y1, x2, y2):
    ''' Retourne les valeurs de a et b de y=ax+b
        à partir des coordonnées de 2 points'''
    a = (y2 - y1) / (x2 - x1)
    b = y1 - (a * x1)
    return a, b

if __name__ == '__main__':
    # Only to test
    spam = 42
    a = 42
    c = [0,0]
    d = {"g":1, "1":2}

    ip =get_my_ip()

    print_str_args("a", "spam", "c", "d", "ip")
    ##print(droiteAffine(0, -30, 0.7, -20))
