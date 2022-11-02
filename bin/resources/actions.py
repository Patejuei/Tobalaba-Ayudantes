import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as db


def men_inf():
    def gen_inf():
        infmen = db.connect("./bin/databases/asistencia.db")
        pers = db.connect("./bin/databases/Relacion de personal.db")
        # DEFINIR CONSTANTES
        cur = infmen.cursor()
        cur2 = pers.cursor()
        mes = mo.index(comb_mo.get()) + 1
        year = int(comb_ye.get())
        # BUSCAR LISTAS EN BASE A LOS PARÁMETROS
        asistencia = []
        for row in cur.execute("""SELECT * FROM Asistencia WHERE MES = {} AND AÑO = {}""".format(mes, year)):
            n = 8
            print(row[n:]) # SELECCIONAR SOLO LOS CAMPOS DE ASISTENCIA
            for asis in cur2.execute("""SELECT REG_GRAL, NOMBRE FROM Relacion_de_Personal"""):
                asistencia.append([asis[0], asis[1], row[n]])
        return
    inf = tk.Tk()
    inf.title("Generar Informe Mensual")
    mo = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
          "Septiembre", "Octubre", "Noviembre", "Diciembre")
    ye = ("2022", "2023", "2024", "2025")
    comb_mo = ttk.Combobox(inf, values=mo)
    comb_ye = ttk.Combobox(inf, values=ye)
    comb_mo.grid(column=0, row=1)
    comb_ye.grid(column=1, row=1)
    ttk.Button(inf, text="Generar", command=gen_inf).grid(column=0, row=2, columnspan=2)
    tk.Label(inf, text="Seleccione Mes de Informe").grid(column=0, row=0, columnspan=2)
    inf.lift()
