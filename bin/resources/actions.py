import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as db
import pandas as pd
import os


class Conexion:
    def __init__(self, host, user, password, database):
        self.connection = db.connect(host=host,
                                     user=user,
                                     password=password,
                                     database=database)

    def connect(self):
        return self.connection


headeractos = ["Reg. Gral. Bombero", "Correlativo Compañia", "Tipo de Acto", "Correlativo General", "Fecha",
               "Direccion", "Lista"]
con = Conexion("127.0.0.1", "root", "root", "asistencia_anual").connect()
cursor = con.cursor()


def inf_men(mo, comb_mo):
    listas = []
    actos = []
    # AGREGA LOS REGISTROS Y NOMBRES A LAS LISTAS
    cursor.execute("SELECT reg_gral, nombre FROM bomberos")
    for row in cursor.fetchall():
        row = list(row)
        listas.append(row)
    mensualPath = "bin/Informes/Asistencia.xlsx"
    month_search = int(mo.index(comb_mo.get()))
    # AGREGA EL CONTEO A LAS LISTAS
    for n in range(len(listas)):
        cursor.execute("""SELECT count(reg_gral_voluntario) FROM asistencia 
                    CROSS JOIN actos 
                    WHERE MONTH(actos.fecha) = %s AND reg_gral_voluntario = %s AND asistencia.corr_cia_acto = actos.corr_cia""",
                       (month_search, listas[n][0]))
        asisvol = cursor.fetchall()
        listas[n].append(asisvol[0][0])
    # AGREGA EL PROMEDIO DE LAS LISTAS
    cursor.execute("SELECT count(lista) FROM actos WHERE  MONTH(actos.fecha) = %s", (month_search,))
    totalListas = cursor.fetchall()
    for n in range(len(listas)):
        listas[n].append((listas[n][2] / totalListas[0][0]))
    # AGREGA LA CANTIDAD DE OBLIGATORIAS
    for n in range(len(listas)):
        cursor.execute("""SELECT count(reg_gral_voluntario) FROM asistencia 
                    CROSS JOIN actos 
                    WHERE MONTH(actos.fecha) = %s AND reg_gral_voluntario = %s AND asistencia.corr_cia_acto = actos.corr_cia AND actos.lista = \"OB\"""",
                       (month_search, listas[n][0]))
        asisvol = cursor.fetchall()
        listas[n].append(asisvol[0][0])

    # AGREGA EL PROMEDIO DE OBLIGATORIAS
    cursor.execute("SELECT count(lista) FROM actos WHERE  MONTH(fecha) = %s AND lista = \"OB\"", (month_search,))
    totalEfectivas = cursor.fetchall()
    for n in range(len(listas)):
        listas[n].append((listas[n][4] / totalEfectivas[0][0]))
    # AGREGA LOS ACTOS DEL PERIODO
    cursor.execute("""SELECT  a.reg_gral_voluntario, actos.corr_cia, actos.acto, actos.corr_gral, actos.fecha, actos.direccion, actos.lista FROM actos
        INNER JOIN asistencia a on actos.corr_cia = a.corr_cia_acto
        WHERE MONTH(fecha) = %s""", (month_search,))
    for row in cursor.fetchall():
        actos.append(row)
    header = ["Reg. Gral", "Nombre", "Listas totales", "Asistencia General", "Listas Obligatorias",
              "Asistencia Obligatorias"]
    listdf = pd.DataFrame(listas)
    actdf = pd.DataFrame(actos)
    xlwriter = pd.ExcelWriter(mensualPath)
    listdf.to_excel(xlwriter, sheet_name="Asistencia Voluntarios", header=header,
                    index=False)
    actdf.to_excel(xlwriter, sheet_name="Actos", header=headeractos, index=False)
    print(listdf)
    xlwriter.close()
    # os.startfile(mensualPath)
    return


def inf_90dias():
    listas = []
    actos = []
    # AGREGA LOS REGISTROS Y NOMBRES A LAS LISTAS
    cursor.execute("SELECT reg_gral, nombre FROM bomberos")
    for row in cursor.fetchall():
        row = list(row)
        listas.append(row)
    ninetyPath = "bin/Informes/Asistencia_90_dias.xlsx"
    for n in range(len(listas)):
        cursor.execute("""SELECT count(reg_gral_voluntario) FROM asistencia 
            INNER JOIN actos 
            ON asistencia.corr_cia_acto = actos.corr_cia
            WHERE actos.fecha <= DATE_ADD(CURDATE(), INTERVAL 90 DAY) AND reg_gral_voluntario = %s""",
                       (listas[n][0],))
        asisvol = cursor.fetchall()
        listas[n].append(asisvol[0][0])
    for n in range(len(listas) - 1, -1, -1):
        if listas[n][2] != 0:
            listas.pop(n)
    # AGREGA LOS ACTOS DEL PERIODO
    cursor.execute("""SELECT a.reg_gral_voluntario, corr_cia, acto, corr_gral, fecha, direccion, lista FROM actos
    INNER JOIN asistencia a on actos.corr_cia = a.corr_cia_acto
    WHERE fecha <= DATE_ADD(CURDATE(), INTERVAL 90 DAY)""")
    for row in cursor.fetchall():
        actos.append(row)
    actdf = pd.DataFrame(actos)
    dias90 = pd.DataFrame(listas)
    header = ["Reg. Gral", "Nombre", "Listas en los 90 Días"]
    writer = pd.ExcelWriter(ninetyPath)
    dias90.to_excel(writer, sheet_name="Informe 90 Dias", header=header,
                    index=False)
    actdf.to_excel(writer, sheet_name="Actos 90 Dias", header=headeractos,
                   index=False)
    writer.close()
    # os.startfile("../" + ninetyPath)
