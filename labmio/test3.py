from tkinter import *
master = Tk()
def callback():
    print("click!")
b = Button(master, text="OK", command=callback, padx=132, pady=132,
activebackground="green", activeforeground="yellow",
background="black", foreground="red"
)
b.pack()
a = Button(master, text="OK", command=callback, padx=132, pady=132,
state=DISABLED, background="black", disabledforeground="blue"
)
a.pack()
mainloop()