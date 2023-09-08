#Ejercicio 1

import sys
if int(sys.argv[1])%2==0:
    print("parámetro 1 tiene valor:", sys.argv[1], "y es un número par")
else:    
    print("parámetro 1 tiene valor:", sys.argv[1], "y es número impar")
if int(sys.argv[2])%2==0:
    print("parámetro 2 tiene valor:", sys.argv[2], "y es número par")
else:    
    print("parámetro 2 tiene valor:", sys.argv[2], "y es número impar")
if int(sys.argv[3])%2==0:
    print("parámetro 3 tiene valor:", sys.argv[3], "y es número par")
else:    
    print("parámetro 3 tiene valor:", sys.argv[3], "y es número impar")

#Ejercicio 2
"""
Cree una lista de frutas de 2 elementos, y realice un programa que muestre una oración
conteniendo los dos elementos de la lista concatenándolos con texto para formar una
oración con sentido. Presente el resultado en la terminal del editor.  
"""
import sys
lista_frutas = ["bananas", "peras"]
print("la lista es: ", lista_frutas)
print("Por suerte conseguí", lista_frutas[0], "y", lista_frutas[1], "en la verdulería.")

#Ejercicio 3
"""
Tome dos valores por consola, y guarde en una lista:
[primer_valor, segundo_valor, la_sum
Presente el resultado en la terminal del editor.
"""
valor1 = int(input("Por favor ingrese el primer valor: "))
valor2 = int(input("Por favor ingrese el segundo valor: "))
lista = [valor1, valor2, valor1 + valor2]
print("La lista:", lista)
Presente el resultado en la terminal del editor.

#Ejercicio 4
"""
Realice un programa que consulte la edad y en caso de que el valor ingresado supere la
fecha de jubilación, presente en la terminal el mensaje
caso contrario que presente “Aún está en edad de trabajar”
"""
edad = int(input("Por favor ingrese su edad: "))
sexo = input("Por favor ingrese F si es mujer y M si es hombre: ")

if sexo == "F":
    edad_jubilarse = 60
else:
    edad_jubilarse = 65

if edad >= edad_jubilarse:    
    print("Ya está en edad de jubilarse")
else:
     print("Aún está en edad de trabajar")
    #print("”)


#Ejercicio 5
#Ejercicio 3 unidad 1
"""
Realice nuevamente los ejercicios de la unidad 1 (3, 4 y 5), pero tratando de utilizar una
función, de forma que la operación se realice dentro de la misma.
"""
""" Antes
num1 = float(input("ingresa el radio de la circunferencia y presione enter: "))
numFinal = 2 *float(3.1416) * num1
print("La longitud del perímetro para el radio ingresado es: ", numFinal)
"""
import math
def calcular_logitud_perimetro(radio):
    numFinal = 2 *float(math.pi) * radio
    return numFinal
    
radio = float(input("ingresa el radio de la circunferencia y presione enter: "))
numFinal = calcular_logitud_perimetro(radio)   
print("La longitud del perímetro para el radio ingresado es: ", numFinal)




# Ejercicio 4 unidad 1
""" antes
import math
num1 = float(input("ingresa el radio de la circunferencia y presione enter: "))
numFinal = float(3.1416) * (num1**2)
print("El área de la circunferencia para el radio ingresado es: ", numFinal)

"""
import math

def calcular_area_circunferencia(radio):
    return float(math.pi) * (radio**2)
    
num1 = float(input("ingresa el radio de la circunferencia y presione enter: "))
numFinal = calcular_area_circunferencia(num1)
print("El área de la circunferencia para el radio ingresado es: ", numFinal)


# Ejercicio 5 unidad 1
""" antes
import math
num1 = input("ingresa un número: ")
numFinal = float(num1) * (1.10)
print("El número incrementado un 10% es: ", numFinal)
"""
import math
def calcular_incremeto_10_porciento(num):
    return float(num1) * (1.10)
    
num1 = input("ingresa un número: ")
numFinal = calcular_incremeto_10_porciento(num1)
print("El número incrementado un 10% es: ", "%.0f" % numFinal)
