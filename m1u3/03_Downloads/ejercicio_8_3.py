compra=[]
total=0


# ############### VISTA #############################
def menu():
    print("\n Elija una opción: ")
    print("    (a) Agregar producto: ")
    print("    (e) Eliminar producto: ")
    print("    (l) Listar producto: ")
    print("    (m) Modificar producto: ")
    print("    ó cualquier otra tecla para salir: ")

    global valor
    global eleccion
    eleccion=input("")
    if eleccion=='a' or eleccion=="e" or eleccion=="l" or eleccion=="m":
        valor=True
    else:
        valor=False
menu()
# ############### MODELO #############################
def alta(producto, cantidad, precio):
    global total
    cantidad=float(cantidad)
    precio=float(precio)
    total=total+cantidad*precio
    compra.append([producto, cantidad, precio])
    print("Estoy dentro de alta")

def borrar():print("eeeeeeeeeeee")

def listar():print("lllllllllllll")

def modificar():print("mmmmmmmmmmmm")

# ############### CONTROLADOR #############################
while valor==True:
    if eleccion=="a":
       producto, cantidad, precio=input("Ingrese nombre de producto cantidad y precio separado por espacio: ").split()
       alta(producto, cantidad, precio)
    elif eleccion=="e":
        borrar()
    elif eleccion=="l":
        listar()
    elif eleccion=="m":
        modificar()
    else:
        break
    menu()


for x in compra:
    print("Producto: ", x[0], "Cantidad: ", x[1], "Precio: ", x[2])

print("El valor total de la compra es: ", total)