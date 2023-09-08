compra=[]
total=0
id=0

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
    global id
    id+=1
    cantidad=float(cantidad)
    precio=float(precio)
    total=total+cantidad*precio
    compra.append([id, producto, cantidad, precio])
    print("Estoy dentro de alta")

def borrar(id_e):
    global total
    global compra
    for x in compra:
        if x[0]==int(id_e):
            compra.remove(x)
            total=total-float(x[2])*float(x[3])
    print("Estoy dentro de listar")

def listar():
     global compra
     global total
     print(compra)
     print(total)
     print("Estoy en listar")

def modificar():print("mmmmmmmmmmmm")

# ############### CONTROLADOR #############################
while valor==True:
    if eleccion=="a":
       producto, cantidad, precio=input("Ingrese nombre de producto cantidad y precio separado por espacio: ").split()
       alta(producto, cantidad, precio)
    elif eleccion=="e":
        id_e=input("Ingrese el identificador del elemento a borrar: ")
        borrar(id_e)
    elif eleccion=="l":
        listar()
    elif eleccion=="m":
        modificar()
    else:
        break
    menu()


for x in compra:
    print("id", x[0], "Producto: ", x[1], "Cantidad: ", x[2], "Precio: ", x[3])

print("El valor total de la compra es: ", total)
print(compra)

"""
[ 
    [1, 'papas', 2.0, 2.0], 
    [2, 'pera', 3.0, 3.0], 
    [3, 'uvas', 4.0, 4.0]
]
"""