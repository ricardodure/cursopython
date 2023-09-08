"""
Ejercicio 6
A partir del ejercicio 5 cree un programa que vaya agregando 
en una lista las compras realizadas.
"""
compra=[]
total=0
valor=False
eleccion=input("Para iniciar ingrese 'i', para finalizar ingrese otra tecla: ")
if eleccion=='i':
    valor=True
else:
    valor=False

while valor==True:
    producto, cantidad, precio=input("Ingrese nombre de producto cantidad y precio separado por espacio: ").split()
    cantidad=float(cantidad)
    precio=float(precio)
    total=total+cantidad*precio
    compra.append([producto, cantidad, precio])
    eleccion=input("Para iniciar ingrese 'i', para finalizar ingrese otra tecla: ")

    if eleccion=='i':
        valor=True
    else:
        valor=False

for x in compra:
    print("Producto: ", x[0], "Cantidad: ", x[1], "Precio: ", x[2])

"""
compra=[
    ["Pera", 2, 2],
    ["Papas", 3, 3]
]
"""

print("El valor total de la compra es: ", total)