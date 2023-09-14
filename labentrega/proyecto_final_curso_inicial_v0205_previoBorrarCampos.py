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
    val_stock.set("")
    val_punto_reposicion.set("")
    val_proveedor.set("")
    val_costo.set("")
    val_precio.set("")

def valida_producto(cadena):
    
    patron ='^[0-9A-Za-záéíóúÁÉÍÓÚñÑ]{1,20}$' #regex para producto
    if not(re.match(patron, cadena)):        
        mb.showerror(title = "Error", message = "Error: El campo Producto debe tener valor y ser alfanúmérico de hasta 20 caracteres.")
        return FALSE
    return TRUE

def valida_largo_y_no_vacio(cadena, largo, desc_campo):
     
    if (len(cadena.strip()) == 0 or len(cadena.strip()) > largo):        
        mb.showerror(title = "Error", message = "Error: El campo {0} debe tener valor y hasta {1} caracteres.".format(desc_campo, largo))
        return FALSE
    return TRUE

def valida_numero(cadena, desc_campo):
    patron_numero = r'^[0-9]*\.?[0-9]+$'
    if (len(cadena.strip()) == 0):
        mb.showerror(title = "Error", message = "Error: El campo {0} no puede ser vacío.".format(desc_campo))
        return FALSE
    
    if not(re.match(patron_numero, cadena)):
        mb.showerror(title = "Error", message = "Error: El campo {0} debe ser numérico (Ej: 3 ó 1.5)".format(desc_campo))
        return FALSE
    
    return TRUE

def validar_carga(producto, descripcion, stock, punto_reposicion, costo, precio):

    #valido producto
    if not(valida_producto(producto)):
        return 1
    
    #valido descripcion    
    if not(valida_largo_y_no_vacio(descripcion, 500, "Descripción")):
        return 1
    
    #valido stock
    if not(valida_numero(stock, "Stock")):
        return 1
    
    #valido punto de reposición
    if not(valida_numero(punto_reposicion, "Punto de Reposición")):
        return 1
    
    #valido stock
    if not(valida_numero(costo, "Costo")):
        return 1
    
    #valido precio
    if not(valida_numero(precio, "Precio")):
        return 1
      
    return 0

def alta(producto, descripcion, stock, punto_reposicion, proveedor, costo, precio, tree):  
   
    if not validar_carga(producto, descripcion, stock, punto_reposicion, costo, precio) == 0:
        return
   
    try:
        con=conexion()
        cursor=con.cursor()
        data=(producto, descripcion.strip(), stock, punto_reposicion, proveedor, costo, precio)
        sql="INSERT INTO productos(producto, descripcion, stock, punto_reposicion, proveedor, costo, precio) VALUES(?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print("Alta exitosa del registro con Producto: {} ,Descripción: {}, Stock: {}, Punto de Reposición: {} ,Proveedor: {}, Costo: {} y Precio: {}".format(producto, descripcion, stock, punto_reposicion, proveedor, costo, precio))
        actualizar_treeview(tree)  

        #Limpio campos de ingreso de datos  
        limpiar_campos()

        elementos = tree.get_children()        
        if elementos:
            last_element = elementos[-1]
            tree.see(last_element)

    except: 
         mb.showerror(title = "Error", message = "Error: No se pudo realizar el Alta. Verifique que el Producto '{}' no esté ya en la lista.".format(producto))
   
def modificacion(producto, descripcion, stock, punto_reposicion, proveedor, costo, precio, tree):  
   
    if not validar_carga(producto, descripcion, stock, punto_reposicion, costo, precio) == 0:
        return
   
    valor = tree.selection()    
    item = tree.item(valor)    
    mi_id = item['text']

    try:
        con=conexion()
        cursor=con.cursor()
        #mi_id = int(mi_id)
        data = (producto, descripcion, stock, punto_reposicion, proveedor, costo, precio, mi_id)
        sql = "UPDATE productos SET producto = ?, descripcion= ?, stock=?, punto_reposicion=?, proveedor=?, costo=?, precio=? WHERE id = ?"
        cursor.execute(sql, data)
        con.commit()        
        if (con.total_changes == 0):
            mb.showerror(title = "Error", message = "Error: No se encontró ningun registro con ID {} para Modificar".format(mi_id))
        actualizar_treeview(tree)
        print("Modificación exitosa del registro con ID: {}".format(mi_id))

        #Limpio campos de ingreso de datos  
        limpiar_campos()
    except:
         mb.showerror(title = "Error", message = "Error: No se pudo realizar la Modificación del registro registro con ID {}".format(mi_id))
      

def consultar(tree):
    actualizar_treeview(tree) 
    print("Consulta exitosa")
   
def borrar(tree):
    valor = tree.selection()    
    item = tree.item(valor)    
    mi_id = item['text']

    try:
        con=conexion()
        cursor=con.cursor()
        #mi_id = int(mi_id)
        data = (mi_id,)
        sql = "DELETE FROM productos WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        print("Baja exitosa del registro con ID: {}".format(mi_id))
        #Limpio campos de ingreso de datos  
        limpiar_campos()
    except:
        #print("Error: No se pudo realizar la Baja {}".format(mi_id))
         mb.showerror(title = "Error", message = "Error: No se pudo realizar la Baja del registro registro con ID {}".format(mi_id))

    
        
def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM productos ORDER BY id DESC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        #print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7]))

def seleccionar_fila(event):
    seleccion = tree.selection()
    if seleccion:
        item = tree.item(seleccion[0])
        val_producto.set(item["values"][0])
        val_descripcion.set(item["values"][1])
        val_stock.set(item["values"][2])
        val_punto_reposicion.set(item["values"][3])
        val_proveedor.set(item["values"][4])
        val_costo.set(item["values"][5])
        val_precio.set(item["values"][6])

try:
    conexion()
    crear_tabla()
except:
    print("Hay un error en la conexión")


# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("Sistema de Stock")
root.eval('tk::PlaceWindow . center')
        
titulo = Label(root, text="Ingrese sus datos", bg="#156a0d", fg="thistle1", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=8, padx=1, pady=1, sticky=W+E)

# Labels de los campos
producto = Label(root, text="Producto")
producto.grid(row=1, column=0, sticky=W)

descripcion=Label(root, text="Descripción")
descripcion.grid(row=2, column=0, sticky=W)

descripcion=Label(root, text="Stock")
descripcion.grid(row=3, column=0, sticky=W)

descripcion=Label(root, text="Punto de Reposición")
descripcion.grid(row=4, column=0, sticky=W)

descripcion=Label(root, text="Proveedor")
descripcion.grid(row=5, column=0, sticky=W)

descripcion=Label(root, text="Costo")
descripcion.grid(row=6, column=0, sticky=W)

descripcion=Label(root, text="Precio")
descripcion.grid(row=7, column=0, sticky=W)

# Defino variables para tomar valores de campos de entrada
val_producto, val_descripcion, val_stock, val_punto_reposicion, val_proveedor, val_costo, val_precio = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar() 
w_ancho = 20

# Campos de Entrada
entrada1 = Entry(root, textvariable = val_producto, width = w_ancho) 
entrada1.grid(row = 1, column = 1)

entrada2 = Entry(root, textvariable = val_descripcion, width = w_ancho) 
entrada2.grid(row = 2, column = 1)

entrada3 = Entry(root, textvariable = val_stock, width = w_ancho) 
entrada3.grid(row = 3, column = 1)

entrada4 = Entry(root, textvariable = val_punto_reposicion, width = w_ancho) 
entrada4.grid(row = 4, column = 1)

entrada5 = Entry(root, textvariable = val_proveedor, width = w_ancho) 
entrada5.grid(row = 5, column = 1)

entrada6 = Entry(root, textvariable = val_costo, width = w_ancho) 
entrada6.grid(row = 6, column = 1)

entrada7 = Entry(root, textvariable = val_precio, width = w_ancho) 
entrada7.grid(row = 7, column = 1)

# Label para mostrar operaciones exitosas
msg_operacion=Label(root, text="La operacion fue un exito")
msg_operacion.grid(row=8, column=0, columnspan = 5, sticky = W + E, padx = 150)

# Botones
boton_alta=Button(root, text="Agregar", command=lambda:alta(val_producto.get(), val_descripcion.get(), val_stock.get(), val_punto_reposicion.get(), val_proveedor.get(), val_costo.get(), val_precio.get(), tree))
boton_alta.grid(row=8, column=0)

boton_modificar=Button(root, text="Modificar", command=lambda:modificacion(val_producto.get(), val_descripcion.get(), val_stock.get(), val_punto_reposicion.get(), val_proveedor.get(), val_costo.get(), val_precio.get(), tree))
boton_modificar.grid(row=8, column=1)

boton_borrar=Button(root, text="Borrar", command=lambda:borrar(tree))
boton_borrar.grid(row=8, column=2)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)
tree["columns"]=("col1", "col2", "col3", "col4", "col5", "col6", "col7")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=50, minwidth=80)
tree.column("col4", width=50, minwidth=80)
tree.column("col5", width=200, minwidth=80)
tree.column("col6", width=50, minwidth=80)
tree.column("col7", width=50, minwidth=80)

tree.heading("#0", text="ID")
tree.heading("col1", text="Producto")
tree.heading("col2", text="Descripción")
tree.heading("col3", text="Stock")
tree.heading("col4", text="Punto de Reposición")
tree.heading("col5", text="Proveedor")
tree.heading("col6", text="Costo")
tree.heading("col7", text="Precio")

tree.grid(row=10, column=0, columnspan=8)
tree.bind("<<TreeviewSelect>>", seleccionar_fila)

actualizar_treeview(tree) # muestro al inicio el treeview por si la base ya está creada y tiene datos

root.mainloop()
