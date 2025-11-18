from tkinter import *

class Test:
    def __init__(self):
        window = Tk()
        window.geometry("1080x920")
        frame1 = Frame(window, bg="blue",width=20,height=100)
        frame1.pack(fill="both")
        window.mainloop()

Test()