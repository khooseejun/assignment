from tkinter import *

window = Tk()
window.title("Python Tkinter Windows")
window.geometry("1080x920")
window.resizable(False,False)
window.config(background="#0C090A")

label = Label(
    window,text="Hello, World!",
    font=("Arial",24,"bold"),
    fg="green",
    bg="blue",
    padx=10,
    pady=10
)
label.pack()

window.mainloop()