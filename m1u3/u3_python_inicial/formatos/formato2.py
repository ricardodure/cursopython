import pprint

anna = {
    "identificacion": {"nombre": "Anna", "apellido": "Rodríguez"},
    "edad": 50,
    "sueldo": 30000,
}
josefa = {
    "identificacion": {"nombre": "Josefa", "apellido": "Rodríguez"},
    "edad": 70,
    "sueldo": 60000,
}
db = {}
db["anna"] = anna
db["josefa"] = josefa
print(db)
print("---" * 23)
pprint.pprint(db)
