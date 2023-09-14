from tkinter import *
master = Tk()
master.geometry("700x500")
def callback():
    print("click!")
b = Button(master, text="OK", command=callback,
activebackground="green", activeforeground="yellow",
background="black", foreground="red", height=7, width=12, anchor=SW)
anchor=SW
b.pack(side=LEFT)
mainloop()