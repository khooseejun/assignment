from tkinter import *

class Test:
    def __init__(self):
        window = Tk()
        frame1 = Frame(window, bg="blue",width=1080,height=920)
        frame1.pack()

        window.mainloop()

Test()