from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as db

cant = 1


def men_inf():
    return 0


def save_li():
    global vols_asis
    list_arr = []
    asis_arr = []
    messagebox.showinfo('Guardar', 'Lista Guardada con Éxito')
    asistencia = db.connect("bin/databases/asistencia.db")
    asistenciacur = asistencia.cursor()
    asis_arr.append(acto.get())
    asis_arr.append(ubi.get())
    if ob:
        asis_arr.append("OB")
    asis_arr.append(dd.get())
    asis_arr.append(mm.get())
    asis_arr.append(yy.get())
    asis_arr.append(in_corr_cia.get())
    asis_arr.append(in_corr_gral.get())
    list_arr.append("ACTO")
    list_arr.append("DIRECCION")
    list_arr.append("OBLIGATORIO")
    list_arr.append("DIA")
    list_arr.append("MES")
    list_arr.append("AÑO")
    list_arr.append("CORR_CIA")
    list_arr.append("CORR_GRAL")
    for i in range(len(vols_asis)):
        if vols_asis[i].get() != "":
            list_arr.append(vols_asis[i].get())
            asis_arr.append("A")
    list_tuple = tuple(list_arr)
    asis_tuple = tuple(asis_arr)
    asistenciacur.execute('INSERT INTO Asistencia {} VALUES {}'.format(list_tuple, asis_tuple))
    asistencia.commit()
    asistencia.close()


def bind_save_li(event):
    save_li()


def new_vol(event):
    global cant
    global asis
    global vols_asis
    global vols
    for i in range(len(vols_asis)):
        if vols_asis[i].get() != "":
            volcur = vols.cursor()
            for row in volcur.execute('SELECT NOMBRE, REG_GRAL FROM Relacion_de_Personal'):
                if row[1] == vols_asis[i].get():
                    Label(asis, text=row[0]).grid(column=1, row=i + 1, columnspan=3, sticky=W)
                    break

    if vols_asis[cant - 1].get() != "" and vols_asis[cant - 1] not in vols_asis:
        cant += 1
        vols_asis.append(Entry(asis, width=10))
        vols_asis[cant - 1].grid(column=0, row=cant, sticky=E)
        vols_asis[cant - 1].bind('<Tab>', new_vol)


if __name__ == '__main__':
    vols = db.connect('bin/databases/Relacion de personal.db')
    root = Tk()
    root.title('Sistema de Registro de Asistencia')
    root.resizable(False, False)
    root.config(padx=5, pady=5)
    # root.iconbitmap()
    gen_inf = ttk.Button(root, text='Generar Informe Mensual', command=men_inf())
    gen_inf.grid(column=0, row=0, sticky=W + E)
    save = ttk.Button(root, text='Guardar (F5)', command=save_li)
    save.grid(column=0, row=1, sticky=W + E)
    ttk.Label(root, text='CORRELATIVO COMPAÑÍA: ').grid(column=1, row=1, sticky=S)
    in_corr_cia = ttk.Entry(root, width=12)
    in_corr_cia.grid(column=2, row=0, rowspan=2, sticky=S)
    ttk.Label(root, text='CORRELATIVO GENERAL: ').grid(column=3, row=0, rowspan=2, sticky=S)
    in_corr_gral = ttk.Entry(root, width=12)
    in_corr_gral.grid(column=4, row=0, rowspan=2, sticky=S)
    ob = Checkbutton(root, text='OBLIGATORIA', takefocus=0)
    ob.grid(column=1, row=0)
    ttk.Label(root, text='DÍA').grid(column=5, row=0)
    ttk.Label(root, text='MES').grid(column=6, row=0)
    ttk.Label(root, text='AÑO').grid(column=7, row=0)
    dd = ttk.Entry(root, width=5)
    dd.grid(column=5, row=1)
    mm = ttk.Entry(root, width=5)
    mm.grid(column=6, row=1)
    yy = ttk.Entry(root, width=5)
    yy.grid(column=7, row=1)
    ttk.Label(root, text='DIRECCIÓN: ').grid(column=0, row=2, sticky=E)
    ubi = ttk.Entry(root, width=30)
    ubi.grid(column=1, row=2, columnspan=3, sticky=E + W)
    ttk.Label(root, text="ACTO: ").grid(column=4, row=2)
    acto = ttk.Entry(root)
    acto.grid(column=5, row=2, columnspan=3)

    # Comienza el ingrerso de asistencia
    asis = Frame(root)
    asis.grid(row=3, column=0, columnspan=5, sticky=W)
    Label(asis, text='ASISTENCIA VOLUNTARIOS.').grid(column=0, columnspan=5, row=0)
    vols_asis = [Entry(asis, width=10, textvariable=StringVar())]
    vols_asis[0].grid(column=0, row=cant, sticky=E)
    vols_asis[0].bind('<Tab>', new_vol)
    vols_asis[cant - 1].bind('<F5>', bind_save_li)

    root.mainloop()
