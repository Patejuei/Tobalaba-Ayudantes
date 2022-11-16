import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as db
import pandas as pd


def men_inf():
    def gen_inf():
        connector = db.connect(host="127.0.0.1",
                               user="root",
                               password="root",
                               database="asistencia_anual")
        cur = connector.cursor()
        listas = []
        month_search = int(mo.index(comb_mo.get()))
        # AGREGA LOS REGISTROS Y NOMBRES A LAS LISTAS
        cur.execute("SELECT reg_gral, nombre FROM bomberos")
        for row in cur.fetchall():
            row = list(row)
            listas.append(row)
        # AGREGA EL CONTEO A LAS LISTAS
        for n in range(len(listas)):
            cur.execute("""SELECT count(reg_gral_voluntario) FROM asistencia 
                        CROSS JOIN actos 
                        WHERE actos.mes = %s AND reg_gral_voluntario = %s AND asistencia.corr_cia_acto = actos.corr_cia""", (month_search, listas[n][0]))
            asisvol = cur.fetchall()
            listas[n].append(asisvol[0][0])
        # AGREGA EL PROMEDIO DE LAS LISTAS
        cur.execute("SELECT count(lista) FROM actos WHERE  mes = %s", (month_search,))
        totalListas = cur.fetchall()
        for n in range(len(listas)):
            listas[n].append((listas[n][2] / totalListas[0][0]) * 100)
        # AGREGA LA CANTIDAD DE OBLIGATORIAS
        for n in range(len(listas)):
            cur.execute("""SELECT count(reg_gral_voluntario) FROM asistencia 
                        CROSS JOIN actos 
                        WHERE actos.mes = %s AND reg_gral_voluntario = %s AND asistencia.corr_cia_acto = actos.corr_cia AND actos.lista = \"OB\"""", (month_search, listas[n][0]))
            asisvol = cur.fetchall()
            listas[n].append(asisvol[0][0])

        # AGREGA EL PROMEDIO DE OBLIGATORIAS
        cur.execute("SELECT count(lista) FROM actos WHERE  mes = %s AND lista = \"OB\"", (month_search,))
        totalEfectivas = cur.fetchall()
        for n in range(len(listas)):
            listas[n].append((listas[n][4] / totalEfectivas[0][0]) * 100)
        header = ["Reg. Gral", "Nombre", "Listas totales", "Asistencia General", "Listas Obligatorias", "Asistencia Obligatorias"]
        listdf = pd.DataFrame(listas)
        print(listdf)
        return

    inf = tk.Tk()
    inf.title("Generar Informe Mensual")
    mo = ("", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
          "Septiembre", "Octubre", "Noviembre", "Diciembre")
    comb_mo = ttk.Combobox(inf, values=mo)
    comb_mo.grid(column=0, row=1)
    ttk.Button(inf, text="Generar", command=gen_inf).grid(column=0, row=2, columnspan=2)
    tk.Label(inf, text="Seleccione Mes de Informe").grid(column=0, row=0, columnspan=2)
    inf.lift()
