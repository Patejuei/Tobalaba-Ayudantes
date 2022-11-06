import sqlite3 as db
import mysql.connector as mysql

rel = db.connect("Relacion de personal.db")
asis = mysql.connect(
    host="127.0.0.1",
    user="root",
    password="P@te1025",
    database="asistencia_anual"
)

relcur = rel.cursor()
asiscur = asis.cursor()

for row in relcur.execute('SELECT * FROM Relacion_de_Personal'):
    asiscur.execute('INSERT INTO bomberos (rut, nombre, reg_gral, reg_compañia) VALUES (%s, %s, %s, %s)', row)
asis.commit()
