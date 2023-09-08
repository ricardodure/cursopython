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
def alta():print("aaaaaaaaaaaaa")

def borrar():print("eeeeeeeeeeee")

def listar():print("lllllllllllll")

def modificar():print("mmmmmmmmmmmm")

# ############### CONTROLADOR #############################
while valor==True:
    if eleccion=="a":
       alta()
    elif eleccion=="e":
        borrar()
    elif eleccion=="l":
        listar()
    elif eleccion=="m":
        modificar()
    else:
        break
    menu()

