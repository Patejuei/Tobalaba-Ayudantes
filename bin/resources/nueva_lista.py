import tkinter as tk
from tkinter import ttk, messagebox
import bin.resources.actions as actions
import bin.resources.menu as menu
import tkcalendar
from datetime import date


class NewList(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.asistencia = actions.Conexion("127.0.0.1", "root", "root", "asistencia_anual")
        self.title('Sistema de Registro de Asistencia')
        self.resizable(False, False)
        self.config(padx=5, pady=5)
        # root.iconbitmap()
        self.cant = 1

        # BOTONES DE ACCIÓN
        frmActo = tk.Frame(self)
        frmActo.grid(column=0, row=0)
        btnNuevo = ttk.Button(frmActo, text='Nuevo (F10)', command=self.newList, takefocus=0, width=20)
        btnNuevo.grid(column=0, row=0)
        btnSave = ttk.Button(frmActo, text='Guardar (F5)', command=self.saveList, takefocus=0, width=20)
        btnSave.grid(column=0, row=1)
        btnBack = ttk.Button(frmActo, text="Volver", command=self.toMainMenu, takefocus=0, width=20)
        btnBack.grid(column=0, row=2)

        # INGRESO DEL CORRELATIVO DE COMPAÑÍA (PK)
        ttk.Label(frmActo, text='CORRELATIVO COMPAÑÍA: ').grid(column=1, row=1, sticky=tk.S)
        self.in_corr_cia = ttk.Entry(frmActo, width=12)
        self.in_corr_cia.grid(column=2, row=0, rowspan=2, sticky=tk.S)

        # INGRESO DEL CORRELATIVO GENERAL
        ttk.Label(frmActo, text='CORRELATIVO GENERAL: ').grid(column=3, row=0, rowspan=2, sticky=tk.S)
        self.in_corr_gral = ttk.Entry(frmActo, width=12)
        self.in_corr_gral.grid(column=4, row=0, rowspan=2, sticky=tk.S)

        # CHECKBOX DE LISTA EFECTIVA
        self.ob = tk.StringVar()
        cb = tk.Checkbutton(frmActo, text='OBLIGATORIA', takefocus=0, variable=self.ob, onvalue="OB", offvalue="AB")
        cb.deselect()
        cb.grid(column=1, row=0)

        # INGRESO DE FECHA DE LA LISTA
        ttk.Label(frmActo, text='FECHA').grid(column=6, row=0)
        self.fecha = tkcalendar.DateEntry(frmActo)
        self.fecha.grid(column=6, row=1, columnspan=2)

        # INGRESO DE DIRECCIÓN DEL ACTO
        ttk.Label(frmActo, text='DIRECCIÓN: ').grid(column=1, row=2, sticky=tk.E)
        self.ubi = ttk.Entry(frmActo, width=30)
        self.ubi.grid(column=2, row=2, columnspan=2, sticky=tk.E + tk.W)

        # INGRESO DE LA CLAVE DE DESPACHO
        ttk.Label(frmActo, text="ACTO: ").grid(column=4, row=2)
        self.acto = ttk.Entry(frmActo)
        self.acto.grid(column=5, row=2, columnspan=3)

        # Comienza el ingrerso de asistencia
        self.asis = tk.Frame(self)
        self.asis.grid(row=1, column=0, columnspan=5, sticky=tk.W)
        tk.Label(self.asis, text='ASISTENCIA VOLUNTARIOS.').grid(column=0, columnspan=5, row=0)
        self.vols_asis = [tk.Entry(self.asis, width=10, textvariable=tk.StringVar(), takefocus="")]
        self.vols_asis[0].grid(column=0, row=self.cant, sticky=tk.E)
        self.vols_asis[0].bind('<Return>', self.new_vol)  # PULSANDO ENTER SE AÑADE OTRO CAMPO
        self.vols_asis[self.cant - 1].bind('<F5>', self.saveList)

        self.mainloop()

    def toMainMenu(self):
        self.destroy()
        menu.Main_menu()
        return

    def newList(self):
        self.destroy()
        NewList()

    def saveList(self, *event):
        try:
            asistenciacur = self.asistencia.connection.cursor()
            asis_arr = [self.in_corr_cia.get(), self.acto.get(), self.in_corr_gral.get(), self.fecha.get_date(),
                        self.ubi.get(), self.ob.get(),
                        self.cant - 1]
            # INSERTAR ACTO
            asistenciacur.execute('INSERT INTO actos VALUES (%s, %s, %s, %s, %s, %s, %s)', asis_arr)
            # INSERTAR ASISTENCIA
            for i in range(len(self.vols_asis)):
                if self.vols_asis[i].get() != "":
                    asistenciacur.execute(
                        """INSERT INTO asistencia (corr_cia_acto, reg_gral_voluntario) VALUES (%s, %s)""",
                        [self.in_corr_cia.get(), self.vols_asis[i].get()])
            self.asistencia.connection.commit()
            self.asistencia.connection.close()
            messagebox.showinfo('Guardar', 'Lista Guardada con Éxito')


        except Exception as e:
            messagebox.showinfo('Guardar', 'Ha ocurrido un error')
        return

    def new_vol(self, *event):
        def setLabels():
            for i in range(len(self.vols_asis)):
                if self.vols_asis[i].get() != "":
                    volcur = self.asistencia.connection.cursor()
                    volcur.execute('SELECT nombre, reg_gral FROM bomberos')
                    result = volcur.fetchall()
                    for row in result:
                        if row[1] == self.vols_asis[i].get():
                            tk.Label(self.asis, text=row[0]).grid(column=1, row=i + 1, columnspan=3, sticky=tk.W + tk.E)
                            break

        def addEntry():
            self.cant += 1
            self.vols_asis.append(tk.Entry(self.asis, width=10, takefocus=1))
            self.vols_asis[self.cant - 1].grid(column=0, row=self.cant, sticky=tk.E)
            self.vols_asis[self.cant - 1].bind('<Return>', self.new_vol)
            self.vols_asis[self.cant - 1].focus_set()

        setLabels()
        if self.vols_asis[self.cant - 1].get() != "":
            addEntry()
        return
