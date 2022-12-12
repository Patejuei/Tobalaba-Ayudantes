import tkinter as tk
from tkinter import ttk, messagebox
import bin.resources.actions as actions
import bin.resources.menu as menu
import tkcalendar
from datetime import date


class eBomberos(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.con = actions.Conexion("127.0.0.1", "root", "root", "asistencia_anual").connect()
        self.cursor = self.con.cursor()
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Movimiento de Bomberos')
        self.resizable(False, False)
        self.config(padx=5, pady=5)
        frmBomberos = tk.Frame(self)
        frmBomberos.grid(column=0, row=0)
        ttk.Label(frmBomberos, text="Registro General:").grid(column=0, row=0)
        ttk.Label(frmBomberos, text="Registro Compañía:").grid(column=0, row=2)
        ttk.Label(frmBomberos, text="Fecha de Ingreso:").grid(column=1, row=2)
        ttk.Label(frmBomberos, text="Nombre(s):").grid(column=0, row=4)
        ttk.Label(frmBomberos, text="Apellido Paterno:").grid(column=0, row=6)
        ttk.Label(frmBomberos, text="Apellido Materno:").grid(column=1, row=6)
        ttk.Label(frmBomberos, text="RUT:").grid(column=0, row=8)
        ttk.Label(frmBomberos, text="eMail:").grid(column=1, row=8)
        self.reg_general = tk.StringVar()
        self.nombre = tk.StringVar()
        self.apellidoP = tk.StringVar()
        self.apellidoM = tk.StringVar()
        self.email = tk.StringVar()
        self.reg_cia = tk.IntVar()
        self.rut = 0
        self.dv = ""
        ttk.Entry(frmBomberos, textvariable=self.reg_general).grid(column=0, row=1, padx=5, pady=2)
        ttk.Entry(frmBomberos, textvariable=self.nombre).grid(column=0, row=5, columnspan=2, sticky=tk.E + tk.W,
                                                                  padx=5, pady=2)
        ttk.Entry(frmBomberos, textvariable=self.apellidoP).grid(column=0, row=7, padx=5, pady=2)
        ttk.Entry(frmBomberos, textvariable=self.apellidoM).grid(column=1, row=7, padx=5, pady=2)
        self.grut = tk.StringVar()
        ttk.Entry(frmBomberos, textvariable=self.grut).grid(column=0, row=9, padx=5, pady=2)
        ttk.Entry(frmBomberos, textvariable=self.email).grid(column=1, row=9, padx=5, pady=2)
        ttk.Entry(frmBomberos, textvariable=self.reg_cia).grid(column=0, row=3)
        self.fIngreso = tkcalendar.DateEntry(frmBomberos)
        self.fIngreso.grid(column=1, row=3)
        ttk.Button(frmBomberos, text="Buscar", command=self.srcVol).grid(column=1, row=1, sticky=tk.W + tk.E)
        ttk.Button(frmBomberos, text="Guardar", command=self.save).grid(column=0, row=10, sticky=tk.W + tk.E)
        ttk.Button(frmBomberos, text="Eliminar", command=self.delete).grid(column=1, row=10, sticky=tk.W + tk.E)
        ttk.Button(frmBomberos, text="Volver", command=self.toMainMenu).grid(column=0, row=11, columnspan=2, sticky=tk.W + tk.E)

    def srcVol(self):
        query = """SELECT * FROM bomberos WHERE reg_gral = %s"""
        try:
            self.cursor.execute(query, (self.reg_general.get(), ))
            vols = self.cursor.fetchall()[0]
        except:
            messagebox.showinfo('Alerta', 'Bombero no encontrado')
            return

        self.nombre.set(vols[1])
        self.apellidoP.set(vols[2])
        self.apellidoM.set(vols[3])
        self.email.set(vols[4])
        self.grut.set(vols[5] + "-" + vols[6])
        self.reg_cia.set(vols[7])
        self.fIngreso.set_date(vols[8])

    def save(self):
        try:
            query = """INSERT INTO bomberos VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            gRut = self.grut.get().split("-")
            self.rut = int(gRut[0])
            self.dv = gRut[1]
            self.cursor.execute(query, (self.reg_general.get(), self.nombre.get(), self.apellidoP.get(), self.apellidoM.get(), self.email.get(), self.rut, self.dv, self.reg_cia.get(), self.fIngreso.get_date()))
        except:
            query = """UPDATE bomberos 
            SET nombre = %s, apellidoP = %s, apellidoM = %s, email = %s, rut = %s, dv = %s, reg_cia = %s, f_ingreso = %s
            WHERE reg_gral = %s"""
            gRut = self.grut.get().split("-")
            self.rut = int(gRut[0])
            self.dv = gRut[1]
            self.cursor.execute(query, (self.nombre.get(), self.apellidoP.get(), self.apellidoM.get(), self.email.get(), self.rut, self.dv, self.reg_cia.get(), self.fIngreso.get_date()))
            self.con.commit()
            return

    def delete(self):
        query = """DELETE FROM asistencia WHERE reg_gral_voluntario = %s"""
        self.cursor.execute(query, (self.reg_general.get(), ))
        self.con.commit()
        query = """DELETE FROM bomberos WHERE reg_gral = %s"""
        self.cursor.execute(query, (self.reg_general.get(), ))
        self.con.commit()
        return

    def toMainMenu(self):
        self.destroy()
        menu.Main_menu()
        return
