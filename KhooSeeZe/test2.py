import tkinter as tk

def on_change(*args):
    print("Selected:", var.get())

root = tk.Tk()
var = tk.StringVar(value="Option 1")
var.trace_add("write", on_change)   # trace_add for Python 3.6+

options = ["Option 1", "Option 2", "Option 3"]
om = tk.OptionMenu(root, var, *options).pack()
root.mainloop()
