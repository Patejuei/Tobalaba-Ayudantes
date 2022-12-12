import tkinter as tk
from tkinter import ttk, messagebox
import bin.resources.actions as actions
import bin.resources.menu as menu
import tkcalendar
from datetime import date


class EditList(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.con = actions.Conexion("127.0.0.1", "root", "root", "asistencia_anual").connect()
        self.cursor = self.con.cursor()
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Editar Listas')
        self.resizable(False, False)
        self.config(padx=5, pady=5)
        frmActo = tk.Frame(self)
        frmActo.grid(column=0, row=0)
        tk.Label(frmActo, text="Correlativo Compañía").grid(column=0, row=0)
        self.fldCCia = tk.IntVar()
        ttk.Entry(frmActo, textvariable=self.fldCCia, width=12).grid(column=1, row=0, sticky=tk.W)
        btnSearch = ttk.Button(frmActo, text="Buscar", command=self.bus_lista)
        btnSearch.grid(column=2, row=0)
        # INGRESO DEL CORRELATIVO GENERAL
        ttk.Label(frmActo, text='CORRELATIVO GENERAL: ').grid(column=0, row=1, sticky=tk.E)
        self.in_corr_gral = tk.IntVar()
        ttk.Entry(frmActo, textvariable=self.in_corr_gral, width=12).grid(column=1, row=1, sticky=tk.W)

        # CHECKBOX DE LISTA EFECTIVA
        self.ob = tk.StringVar()
        self.cb = tk.Checkbutton(frmActo, text='OBLIGATORIA', takefocus=0, variable=self.ob, onvalue="OB",
                                 offvalue="AB")
        self.cb.deselect()
        self.cb.grid(column=2, row=1)

        # INGRESO DE FECHA DE LA LISTA
        ttk.Label(frmActo, text='FECHA').grid(column=4, row=1)
        self.fecha = tkcalendar.DateEntry(frmActo)
        self.fecha.grid(column=5, row=1, columnspan=2)

        # INGRESO DE DIRECCIÓN DEL ACTO
        ttk.Label(frmActo, text='DIRECCIÓN: ').grid(column=0, row=2, sticky=tk.E)
        self.ubi = tk.StringVar()
        ttk.Entry(frmActo, textvariable=self.ubi).grid(column=1, row=2, columnspan=3, sticky=tk.E + tk.W)

        # INGRESO DE LA CLAVE DE DESPACHO
        ttk.Label(frmActo, text="ACTO: ").grid(column=4, row=2)
        self.acto = tk.StringVar()
        ttk.Entry(frmActo, textvariable=self.acto).grid(column=5, row=2, columnspan=3, sticky=tk.W)

        # LISTA DE VOLUNTARIOS
        self.lista = ttk.Treeview(frmActo, columns=("reg", "name"), show='headings', height=10)
        self.lista.heading('reg', text="N° de Registro")
        self.lista.heading('name', text="Nombre")
        self.lista.grid(column=0, row=3, columnspan=5, rowspan=5, padx=5, pady=5)

        # AGREGAR VOLUNTARIO
        self.added = tk.StringVar()
        ttk.Entry(frmActo, textvariable=self.added).grid(column=5, row=3, padx=5, sticky=tk.W + tk.E + tk.S)
        ttk.Button(frmActo, text="Añadir", command=self.add_vol).grid(column=5, row=4, padx=5,
                                                                      sticky=tk.W + tk.E + tk.N)

        # BOTONES DE ACCION
        ttk.Button(frmActo, text="Eliminar", command=self.del_vol).grid(column=5, row=5, pady=5, padx=5,
                                                                        sticky=tk.W + tk.E)
        ttk.Button(frmActo, text="Guardar", command=self.update_acto).grid(column=5, row=6, pady=5, padx=5,
                                                                           sticky=tk.W + tk.E)
        ttk.Button(frmActo, text="Volver", command=self.toMainMenu).grid(column=5, row=7, pady=5, padx=5,
                                                                         sticky=tk.W + tk.E)

    def del_lista(self):
        registro = self.lista.get_children()
        for vol in registro:
            self.lista.delete(vol)

    def bus_lista(self):
        query = """SELECT acto, corr_gral, fecha, direccion, lista FROM actos WHERE corr_cia = %s"""
        try:
            self.cursor.execute(query, (self.fldCCia.get(),))
            cont_acto = self.cursor.fetchall()[0]
        except:
            messagebox.showinfo('Error', 'Correlativo no encontrado')
            return

        # SETTING DE INFORMACIÓN
        self.acto.set(cont_acto[0])
        self.in_corr_gral.set(cont_acto[1])
        self.fecha.set_date(cont_acto[2])
        self.ubi.set(cont_acto[3])
        if cont_acto[4] == "AB":
            self.cb.deselect()
        else:
            self.cb.select()
        self.llena_tabla()

    def llena_tabla(self):
        self.del_lista()
        query = """SELECT * FROM bomberos
                INNER JOIN asistencia a 
                on bomberos.reg_gral = a.reg_gral_voluntario
                WHERE a.corr_cia_acto = %s
                ORDER BY a.reg_gral_voluntario"""
        self.cursor.execute(query, (self.fldCCia.get(),))
        dbrows = self.cursor.fetchall()
        for row in dbrows:
            self.lista.insert("", tk.END, values=row[:2])

    def update_acto(self):
        query = """UPDATE actos
        SET acto = %s, corr_gral = %s, fecha = %s, direccion = %s, lista = %s
        WHERE corr_cia = %s"""
        self.cursor.execute(query, (
        self.acto.get(), self.in_corr_gral.get(), self.fecha.get_date(), self.ubi.get(), self.ob.get(),
        self.fldCCia.get()))
        self.con.commit()

    def add_vol(self):
        query = """INSERT INTO asistencia VALUES (default, %s, %s)"""
        self.cursor.execute(query, (self.fldCCia.get(), self.added.get()))
        self.con.commit()
        self.llena_tabla()
        self.added.set("")

    def del_vol(self):
        try:
            self.lista.item(self.lista.selection())['values'][0]
        except IndexError as e:
            messagebox.showinfo('Error', 'Debe seleccionar un voluntario')
            return
        query = """DELETE FROM asistencia WHERE reg_gral_voluntario = %s AND corr_cia_acto = %s"""
        reg = self.lista.item(self.lista.selection())['values'][0]
        self.cursor.execute(query, (reg, self.fldCCia.get()))
        self.con.commit()
        self.llena_tabla()

    def toMainMenu(self):
        self.destroy()
        menu.Main_menu()
        return
