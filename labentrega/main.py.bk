from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox as mb
import sqlite3
from tkinter import ttk
import re

# ##############################################
# MODELO
# ##############################################
def conexion():
    con = sqlite3.connect("stock.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS productos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             producto varchar(20) NOT NULL UNIQUE,
             descripcion varchar(500) NOT NULL,
             stock real not null DEFAULT 0,
             punto_reposicion real,
             proveedor varchar(500),
             costo real,
             precio real)
    """
    cursor.execute(sql)
    con.commit()

def limpiar_campos():
    val_producto.set("") 
    val_descripcion.set("")  

def notificacion_evento_realizado(mensaje):
    msg_operacion.config(text=mensaje)
    #msg_operacion.config(fg='#116158', bg='#d4edda') #, font=('Consolas',11)       
    #msg_operacion.config(fg='#156a0d', bg='#cff771') #, font=('Consolas',11)       
    msg_operacion.config(fg='#116158', bg='#b3f6c3') #, font=('Consolas',11)       
    

def validar_alta(producto, descripcion):  

    #valido producto
    cadena = producto
    patron ='^[0-9A-Za-záéíóúÁÉÍÓÚñÑ]{1,20}$' #regex para producto    
    if not(re.match(patron, cadena)):        
        mb.showerror(title = "Error", message = "Error: El campo Producto debe tener valor y ser alfanúmérico de hasta 20 caracteres.")
        return 1
    
    #valido descripcion
    if (len(descripcion.strip()) == 0):        
        mb.showerror(title = "Error", message = "Error: El campo Descripción debe tener valor y hasta 500 caracteres.")
        return 1
    
    return 0

def validar_modificacion(id, producto, descripcion): 
    # Valido id
    if (id == ""):
       mb.showerror(title = "Error", message = "Error: Debe seleccionar un Producto a modificar de la lista.")
       return 1 

    #valido producto
    cadena = producto
    patron ='^[0-9A-Za-záéíóúÁÉÍÓÚñÑ]{1,20}$' #regex para producto    
    if not(re.match(patron, cadena)):        
        mb.showerror(title = "Error", message = "Error: El campo Producto debe tener valor y ser alfanúmérico de hasta 20 caracteres.")
        return 1
    
    #valido descripcion
    if (len(descripcion.strip()) == 0):        
        mb.showerror(title = "Error", message = "Error: El campo Descripción debe tener valor y hasta 500 caracteres.")
        return 1
    
    return 0

def validar_baja(id):
    # Valido id
    if (id == ""):
       mb.showerror(title = "Error", message = "Error: Debe seleccionar un Producto a eliminar de la lista.")
       return 1
    
    return 0    


def alta(producto, descripcion, tree):  
   
    if not validar_alta(producto, descripcion) == 0:
        return
   
    try:
        con=conexion()
        cursor=con.cursor()
        data=(producto, descripcion.strip())
        sql="INSERT INTO productos(producto, descripcion) VALUES(?, ?)"
        cursor.execute(sql, data)
        con.commit()
        mensaje = "Alta exitosa del Producto: {} y Descripción {}".format(producto, descripcion)
        #print(mensaje)                
        notificacion_evento_realizado(mensaje)
        actualizar_treeview(tree)  

        #Limpio campos de ingreso de datos  
        limpiar_campos()
    except: 
         notificacion_evento_realizado("")
         mb.showerror(title = "Error", message = "Error: No se pudo realizar el Alta. Verifique que el Producto '{}' no esté ya en la lista.".format(producto))
         
   
def modificacion(producto, descripcion, tree):  
      
    valor = tree.selection()    
    item = tree.item(valor)    
    mi_id = item['text']

    if not validar_modificacion(mi_id, producto, descripcion) == 0:
        return

    try:
        con=conexion()
        cursor=con.cursor()
        #mi_id = int(mi_id)
        data = (producto, descripcion, mi_id)
        sql = "UPDATE productos SET producto = ?, descripcion= ? WHERE id = ?"
        cursor.execute(sql, data)
        con.commit()        
        if (con.total_changes == 0):
            mb.showerror(title = "Error", message = "Error: No se encontró ningun Producto con ID {} para Modificar".format(mi_id))
        actualizar_treeview(tree)
        mensaje = "Modificación exitosa del registro con ID: {}".format(mi_id)
        #print(mensaje)
        notificacion_evento_realizado(mensaje)
    except:
         notificacion_evento_realizado("")
         mb.showerror(title = "Error", message = "Error: No se pudo realizar la Modificación del Producto con ID {}".format(mi_id))
      

def consultar(tree):
    actualizar_treeview(tree) 
    print("Consulta exitosa")
   
def borrar(tree):
    valor = tree.selection()
    item = tree.item(valor)    
    mi_id = item['text']

    if not validar_baja(mi_id) == 0:
        return

    try:
        con=conexion()
        cursor=con.cursor()
        #mi_id = int(mi_id)
        data = (mi_id,)
        sql = "DELETE FROM productos WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        mensaje = "Baja exitosa del Producto con ID: {}".format(mi_id)
        #print(mensaje)        
        notificacion_evento_realizado(mensaje)
    except:
        notificacion_evento_realizado("")
        mb.showerror(title = "Error", message = "Error: No se pudo realizar la Baja del Producto con ID {}".format(mi_id))
        
def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM productos ORDER BY id ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        #print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2]))

try:
    conexion()
    crear_tabla()
    print("Conexión exitosa a la base de datos") 
except:    
    mb.showerror(title = "Error", message = "Hay un error en la conexión o creación de la tabla")
    

# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("Sistema de Stock")
root.eval('tk::PlaceWindow . center')
        
titulo = Label(root, text="Ingrese sus datos", bg="#2990b3", fg="thistle1", height=1, width=60) #bg="#156a0d"
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

# Labels de los campos
producto = Label(root, text="Producto")
producto.grid(row=1, column=0, sticky=W)

descripcion=Label(root, text="Descripción")
descripcion.grid(row=2, column=0, sticky=W)

# Defino variables para tomar valores de campos de entrada
val_producto, val_descripcion = StringVar(), StringVar()
w_ancho = 20

# Campos de Entrada
entrada1 = Entry(root, textvariable = val_producto, width = w_ancho) 
entrada1.grid(row = 1, column = 1)

entrada2 = Entry(root, textvariable = val_descripcion, width = w_ancho) 
entrada2.grid(row = 2, column = 1)

# Label para notificación de evento realizado
msg_operacion=Label(root, text="")
msg_operacion.grid(row=9, column=0, columnspan = 4, sticky = W + E, padx = 150)

# Botones
boton_alta=Button(root, text="Agregar", command=lambda:alta(val_producto.get(), val_descripcion.get(), tree))
boton_alta.grid(row=10, column=0)

boton_modificar=Button(root, text="Modificar", command=lambda:modificacion(val_producto.get(), val_descripcion.get(), tree))
boton_modificar.grid(row=10, column=1)

boton_borrar=Button(root, text="Borrar", command=lambda:borrar(tree))
boton_borrar.grid(row=10, column=2)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)
tree["columns"]=("col1", "col2")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)

tree.heading("#0", text="ID")
tree.heading("col1", text="Producto")
tree.heading("col2", text="Descripción")

tree.grid(row=13, column=0, columnspan=3)

actualizar_treeview(tree) # muestro al inicio el treeview por si la base ya está creada y tiene datos

# Función asociada al evento select del treeview
def on_select_treeview(event):
    tree = event.widget

    # No lo dejo seleccionar más de un producto a la vez
    selections = tree.selection()
    if (len(selections) > 1):
        notificacion_evento_realizado("")
        mb.showerror(title = "Error", message = "Debe seleccionar sólo un Producto la lista")
        return
        
    selection = [tree.item(item)["text"] for item in tree.selection()]    
    #print("selected items:", selection)
    valor = tree.selection()
    item = tree.item(valor)    
    mi_id = item['text']    
    
    # Para evitar error de programa cuando se elimina el producto seleccionado 
    old_values = tree.item(valor, 'values')    
    if (len(old_values) == 0):        
        return
    
    mensaje = "Seleccionó el Producto con ID: {}".format(mi_id)    
    notificacion_evento_realizado(mensaje)
    
    # Seteo los valores seleccionados en los campos del formulario
    val_producto.set(old_values[0]) 
    val_descripcion.set(old_values[1]) 

# On select del treeview
tree.bind("<<TreeviewSelect>>", on_select_treeview)

root.mainloop()


