from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re

mi_dic = {}
el_id = 0


def conectando():
    con = sqlite3.connect("alumnos.db")    # Creacion de la db
    return con


def creando_tabla():
    con = conectando()
    cursor = con.cursor()   # Funciona como iterador en la db
    base = ("""CREATE TABLE alumnos_bachiller
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno varchar(20) NOT NULL,
            apellido VARCHAR(20),
            edad INTEGER)""")         # Creación de la tabla que estará en la db
    cursor.execute(base)
    con.commit()


try:
    conectando()
    creando_tabla()
except:
    print("Tenemos un error")


def alta(alumno, apellido, edad, tree):
    global el_id
    global mi_dic
    mi_cad = alumno
    mi_patron = "^[A-Za-záéíóú]*$" # Especifico con regex los simbolos a buscar en la cadena
    if re.match(mi_patron, mi_cad):    # Indico con if, que si el patron está en la cad realice lo ste
        print(alumno, apellido, edad)
        con = conectando()
        cursor = con.cursor()
        data = (alumno, apellido, edad)
        base = ("INSERT INTO alumnos_bachiller(alumno, apellido, edad) VALUES(?, ?, ?) ")
        cursor.execute(base, data)
        con.commit()
        print("Hasta ahora bien")
        el_id += 1
        mi_dic[el_id] = {"Alumno": alumno, "Apellido": apellido, "Edad": edad}
        actualizar_tree(tree)
        print(mi_dic)
        nombre.set("")
        last_name.set("")
        str(age_alumno)
        age_alumno.set("")
    else:
        print("Error de campo")


def actualizar_tree(mi_tree):
    registro = mi_tree.get_children()
    for element in registro:
        mi_tree.delete(element)
    base = "SELECT * FROM alumnos_bachiller ORDER BY id ASC"
    con = conectando()
    un_cursor = con.cursor()
    datos = un_cursor.execute(base)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mi_tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))


def borrar(tree):
    valor = tree.selection()
    print(valor)
    item = tree.item(valor)
    mi_id = item["text"]

    con = conectando()
    cursor = con.cursor()
    data = (mi_id,)
    base = "DELETE FROM alumnos_bachiller WHERE id = ?"
    cursor.execute(base, data)
    con.commit()
    tree.delete(valor)


def color():
    head.config(bg="#1BDB18")


head = Tk()
head.config(background="black")

nombre = StringVar()
last_name = StringVar()
age_alumno = IntVar()

id1 = Label(head, text="Nombre")
id1.grid(row=0, column=0, sticky=E)
id2 = Label(head, text="Apellido")
id2.grid(row=1, column=0, sticky=E)
id3 = Label(head, text="Edad")
id3.grid(row=2, column=0, sticky=E)

entry_id1 = Entry(head, textvariable=nombre)
entry_id1.grid(row=0, column=1)
entry_id2 = Entry(head, textvariable=last_name)
entry_id2.grid(row=1, column=1)
entry_id3 = Entry(head, textvariable=age_alumno)
entry_id3.grid(row=2, column=1)


tree = ttk.Treeview(head)
tree["column"] = ("colu1", "colu2", "colu3")
tree.column("#0", width=50, minwidth=50, anchor=W)
tree.column("colu1", width=80, minwidth=80, anchor=W)
tree.column("colu2", width=80, minwidth=80, anchor=W)
tree.column("colu3", width=100, minwidth=100, anchor=W)

tree.grid(row=5, column=0, columnspan=4)

boton_g = Button(head, text="Guardar", command=lambda:alta(nombre.get(),
                                                           last_name.get(),
                                                           age_alumno.get(),
                                                           tree),
                 padx=10, pady=5)
boton_g.grid(row=3, column=1)

boton_b = Button(head, text="Borrar", command=lambda:borrar(tree), padx=15, pady=5)
boton_b.grid(row=3, column=0)

boton_p = Button(head, text="Personalizar", command=color, padx=15, pady=5)
boton_p.grid(row=3, column=2)

boton_c = Button(head, text="Cerrar", command=quit, padx=15, pady=5)
boton_c.grid(row=10, column=1)

head.mainloop()