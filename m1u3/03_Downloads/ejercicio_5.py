"""
Ejercicio 5
Suponga que tiene una verdulería y carga la cantidad y el precio
de lo comprado por un cliente. Realice un programa que tome
de a uno la cantidad y el precio comprado por el cliente y
al finalizar la compra retorne el monto total gastado. 
"""
total=0
valor=False
eleccion=input("Para iniciar ingrese 'i', para finalizar ingrese otra tecla: ")
if eleccion=='i':
    valor=True
else:
    valor=False

while valor==True:
    cantidad=float(input("Ingrese la cantidad: "))
    precio=float(input("Ingrese el precio: "))
    total=total+cantidad*precio
    
    eleccion=input("Para iniciar ingrese 'i', para finalizar ingrese otra tecla: ")

    if eleccion=='i':
        valor=True
    else:
        valor=False


print("El valor total de la compra es: ", total)