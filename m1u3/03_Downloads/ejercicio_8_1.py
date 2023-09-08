"""
Ejercicio8
A partir del ejerció 6 cree un programa con 4 funciones:
alta() para dar de alta la nueva compra
baja() para dar de baja una compra
consulta() para consultar por todas las compras realizadas hasta el momento
modificar() para modificar una compra realizada

"""
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


# ############### CONTROLADOR #############################
while valor==True:
    if eleccion=="a":
       print("aaaaaaaaaaaaa")
    elif eleccion=="e":
        print("eeeeeeeeeeeeeeeee")
    elif eleccion=="l":
        print("lllllllllllll")
    elif eleccion=="m":
        print("mmmmmmmmmmmmmmmmm")
    else:
        break
    menu()


    """producto, cantidad, precio=input("Ingrese nombre de producto cantidad y precio separado por espacio: ").split()
    cantidad=float(cantidad)
    precio=float(precio)
    total=total+cantidad*precio
    compra.append([producto, cantidad, precio])
    eleccion=input("Para iniciar ingrese 'i', para finalizar ingrese otra tecla: ")

    if eleccion=='i':
        valor=True
    else:
        valor=False"""
"""
for x in compra:
    print("Producto: ", x[0], "Cantidad: ", x[1], "Precio: ", x[2])


compra=[
    ["Pera", 2, 2],
    ["Papas", 3, 3]
]


print("El valor total de la compra es: ", total)"""