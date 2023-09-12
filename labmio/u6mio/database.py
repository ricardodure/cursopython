import sqlite3

def obtener_conexion():
    con = sqlite3.connect("alumnos.db")
    return con

def crear_tabla():
    con = obtener_conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE alumnos_bachiller
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno varchar(20) NOT NULL,
            apellido VARCHAR(20),
            edad INTEGER)"""
    cursor.execute(sql)
    con.commit()

def insert(alumno, apellido, edad):
        con = obtener_conexion()
        cursor = con.cursor()
        data = (alumno, apellido, edad)
        sql = ("INSERT INTO alumnos_bachiller(alumno, apellido, edad) VALUES(?, ?, ?) ")
        cursor.execute(sql, data)
        con.commit()


def delete(mi_id):
    con = obtener_conexion()
    cursor = con.cursor()
    data = (mi_id,)
    sql = "DELETE FROM alumnos_bachiller WHERE id = ?"
    cursor.execute(sql, data)
    con.commit()

def select():
    sql = "SELECT * FROM alumnos_bachiller ORDER BY id ASC"
    con = obtener_conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    resultado = datos.fetchall()
    return resultado    
