import tkinter as tk
from tkinter import ttk, messagebox
import bin.resources.actions as actions
import bin.resources.menu as menu


def informe90Dias():
    actions.inf_90dias()


class InformesWin(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Generar Informes')
        self.resizable(False, False)
        self.config(padx=5, pady=5)
        mensual = tk.LabelFrame(self, text="Informe Mensual")
        mensual.grid(column=0, row=0, pady=5, padx=5)
        self.mo = ("", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                   "Septiembre", "Octubre", "Noviembre", "Diciembre")
        self.comb_mo = ttk.Combobox(mensual, values=self.mo, width=25)
        self.comb_mo.grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(mensual, text="Generar", command=self.generarInforme, width=25).grid(column=0, row=2, padx=5, pady=5)
        tk.Label(mensual, text="Seleccione Mes de Informe").grid(column=0, row=0, columnspan=2)
        oInformes = tk.LabelFrame(self, text="Otros Informes")
        oInformes.grid(column=1, row=0, padx=5, pady=5)
        ttk.Button(oInformes, text="Informe 90 Dias", command=informe90Dias, width=25).grid(column=0, row=0, pady=5, padx=5)
        ttk.Button(oInformes, text="Informe Anual", width=25).grid(column=0, row=1, pady=5, padx=5)
        ttk.Button(oInformes, text="Volver", command=self.back, width=25).grid(column=0, row=2, pady=5, padx=5)

    def generarInforme(self):
        actions.inf_men(self.mo, self.comb_mo)

    def back(self):
        self.destroy()
        menu.Main_menu()

    def send_mail(self):
        emisor = ""
        body = """"""
