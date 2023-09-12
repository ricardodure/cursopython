# Imports
from tkinter import *
from tkinter.colorchooser import askcolor

# Functions
def fun_alta():
    val1 = var_titulo.get()
    val2 = var_ruta.get()
    val3 = var_descripcion.get()
    print("Titulo: ",val1 ," Ruta: ",val2, " Descripcion: ", val3)

def fun_sorpresa():
    result = askcolor(color="#00ff00",title = "Selección de color")
    master.configure(background=result[1])

# APP
master = Tk()

# APP config
master.title("Ejercicio Desafio")
#master.geometry("400x140")  # acá defino el tamaño de la ventana
master['pady'] = 10
master['padx'] = 10

# Variables
var_titulo = StringVar()
var_ruta = StringVar()
var_descripcion = StringVar()

# Labels
lab_titulo_general = Label(master, text="Ingrese sus Datos", bg="#6600ff", fg="#ffffff",height=1, width=80)
lab_titulo_general.grid(row=0, columnspan=3)
lab_titulo = Label(master, text="Título")
lab_titulo.grid(row=1, column=0, sticky=W, padx=[0, 35])
lab_ruta = Label(master, text="Ruta")
lab_ruta.grid(row=2, column=0, sticky=W, padx=[0, 35])
lab_descripcion = Label(master, text="Descripcion")
lab_descripcion.grid(row=3, column=0, sticky=W, padx=[0, 35])

# Entries
ent_titulo = Entry(master, textvariable=var_titulo, width=30)
ent_titulo.grid(row=1, column=1)
ent_ruta = Entry(master, textvariable=var_ruta, width=30)
ent_ruta.grid(row=2, column=1)
ent_descripcion = Entry(master, textvariable=var_descripcion, width=30)
ent_descripcion.grid(row=3, column=1)

# Buttons
but_alta = Button(master, text="Alta", command=fun_alta)
but_alta.grid(row=4, column=1)
but_sorpresa = Button(master, text="Sorpresa", command=fun_sorpresa, width=15)
but_sorpresa.grid(row=4, column=2, padx=50)

# End mainloop
master.mainloop()
