from tkinter import *

master = Tk()

def callback():
    print("click!")

frame = Frame(master)  # Crear un contenedor (marco)
frame.pack()

b = Button(frame, text="OK", command=callback, padx=132, pady=132,
           activebackground="green", activeforeground="yellow",
           background="black", foreground="red")
b.pack(side=LEFT)  # Empaquetar el botón a la izquierda dentro del contenedor

a = Button(frame, text="OK", command=callback, padx=132, pady=132,
           state=DISABLED, background="black", disabledforeground="blue")
a.pack(side=LEFT)  # Empaquetar el segundo botón a la izquierda dentro del contenedor

mainloop()
