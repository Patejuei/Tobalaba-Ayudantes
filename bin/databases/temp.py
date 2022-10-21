import sqlite3 as db

rel = db.connect("Relacion de personal.db")
asis = db.connect("asistencia.db")

relcur = rel.cursor()
asiscur = asis.cursor()

for row in relcur.execute('SELECT REG_GRAL FROM Relacion_de_Personal'):
    asiscur.execute('ALTER TABLE Asistencia ADD COLUMN "%s" TEXT' % row)
