import tkinter as tk
import bin.resources.informes as informes
import bin.resources.nueva_lista as nueva_lista
import bin.resources.EditList as editar_lista
import bin.resources.eBomberos as eBomberos


class Main_menu(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Sistema de Ayudantía Bomba Tobalaba")
        self.config(width=600, height=400)
        self.resizable(False, False)
        container = tk.Frame(self, height=400, width=600)
        container.grid(column=0, row=0, padx=25, pady=25)
        btnNewList = tk.Button(container, text="Nueva Lista", command=self.openNewList, width=25)
        btnEditList = tk.Button(container, text="Editar Lista", command=self.openEditList, width=25)
        btnInformes = tk.Button(container, text="Generar Informes", command=self.openGenInform, width=25)
        btnNewVol = tk.Button(container, text="Editar Bomberos", command=self.addVolunteer, width=25)
        btnInformes.grid(column=0, row=2, padx=5, pady=5)
        btnEditList.grid(column=0, row=1, padx=5, pady=5)
        btnNewList.grid(column=0, row=0, padx=5, pady=5)
        btnNewVol.grid(column=0, row=3, padx=5, pady=5)
        self.mainloop()

    def openNewList(self):
        self.destroy()
        nueva_lista.NewList()

    def openEditList(self):
        self.destroy()
        editar_lista.EditList()
        return

    def openGenInform(self):
        self.destroy()
        informes.InformesWin()
        return

    def addVolunteer(self):
        self.destroy()
        eBomberos.eBomberos()
        return


if __name__ == '__main__':
    Main_menu()
