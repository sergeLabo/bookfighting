## database.py

""" Interface pour communication avec une base sqlite en mémoire"""

import sqlite3

class Mabase():
    """ Interface pour communication avec une base sqlite en mémoire """
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')

    def executescript(self, sql):
        """ Exécute toutes les requêtes SQL.
        executescript() is a nonstandard shortcut that creates an intermediate cursor object
        by calling the cursor method, then calls the cursor’s executescript method with the
        parameters given."""
        print("Requête sql = ", sql)
        c = self.conn.cursor()
        try:
            with self.conn:
                c.executescript(sql)
        except :
            print("Erreur lors de l'excécution de: ", sql)
        c.close()

    def creer(self, table):
        self.executescript(table)

    def inserer(self, valeurs):
        self.executescript(valeurs)

    def lire(self, table):
        c = self.conn.cursor()
        c.execute("SELECT * FROM "+ table)
        for row in c:
            print("Rangée :", row)
        c.close()

# only to test
if __name__ == '__main__':

    from sometools import VirtualGl
    # Création de gl virtuel
    gl = VirtualGl()
    print("gl =", gl)

    # Création de l'instance de classe
    gl.mabase = Mabase()
    print('gl.mabase =', gl.mabase)

    print("\n Création de phone")
    gl.mabase.creer('CREATE TABLE phone (ip text,accx REAL,accy REAL,accz REAL,x REAL,y REAL,t REAL)')

    from time import time
    # enregistrement
    sql = "INSERT INTO phone(ip, accx, accy, accz, x, y, t) VALUES('192.168.1.7', 2.3, 2.3, 2.3, 2.3, 2.3, 1000)"
    gl.mabase.inserer(sql)


    table_name = "phone"
    data = ["192.168.1.7", 2.3, 5.6, 3.4, 0.5, 0.9, time()]
    sql1 = "INSERT into "+table_name+" values ("
    for item in data:
        if type(item) == int:
            sql1 = sql1 + str(item) + ","
        else:
            sql1 = sql1 + "'" + str(item) + "'"+ ","
    sql1 = sql1[:-1] + ")"
    print("sql1 =", sql1)

    gl.mabase.inserer(sql1)

    gl.mabase.lire("phone")
