from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

window = Tk()
window.title("Python Tkinter Windows")
window.geometry("1366x1024")
window.resizable(False,False)
window.config(background="light blue")

option = ["Main", "Sub", "Settings"]

frame = Frame(window)
frame.place(x=0, y=0)

# Label
label = Label(
    frame,text="Hello, World!",
    font=("Arial",24,"bold"),
    fg="green",
    bg="blue",
    padx=10,
    pady=10
)
label.pack(side=LEFT)

# Button
def buttonclick():
    print("Button Clicked")

button = Button(
    frame,
    text="Click Me",
    command=buttonclick,
    fg="green",
    bg="blue",
    activebackground="white"
)
button.pack(side=BOTTOM)

# Entry
def submit():
    thetext = entry.get()
    print(thetext)
    entry.config(state=DISABLED)

def delete():
    entry.delete(0,END)
    print("Text deleted")

def backspace():
    entry.delete(len(entry.get())-1,END)
    print("Delete one symbol")

entry = Entry(
    window,
    font=("Arial",24),
    fg="White",
    bg="grey",
    show="*"
)
entry.pack(side=LEFT)
entry.insert(0,"Hello, World!")

submit_button=Button(
    window,
    text="Submit",
    command=submit
)
submit_button.pack(side=RIGHT)

delete_button=Button(
    window,
    text="Delete",
    command=delete
)
delete_button.pack(side=RIGHT)

backspace_button=Button(
    window,
    text="Backspace",
    command=backspace
)
backspace_button.pack(side=RIGHT)

# Check Button
on_or_off = IntVar()

def buttonstatus():
    if (on_or_off.get() == 1):
        print("Agree")
    else:
        print("Disagree :(")

thecheckbutton = Checkbutton(
    window,
    text="I agree the terms and condition.",
    variable=on_or_off,
    onvalue=1,
    offvalue=0,
    command=buttonstatus
)
thecheckbutton.pack(side=BOTTOM)

# Radio Button ( same as check button, but only 1 active )
radiostatus = IntVar()
def whichoption():
    whichoption_value = radiostatus.get()
    match radiostatus.get():
        case 0:
            print("Radiobutton first option")
        case 1:
            print("Radiobutton second option")
        case 2:
            print("Radiobutton third option")
        case _:
            print("Buggggg")

for i in range(len(option)):
    radiobutton = Radiobutton(
        window,
        text=option[i],
        variable=radiostatus,
        value=i,
        indicatoron=0,
        command=whichoption
    )
    radiobutton.pack(anchor=W)

# Scale
def scalevalue():
    print(scale.get())

scale = Scale(
    window,
    from_=100,
    to=0,
    length=300,
    orient=VERTICAL,
    tickinterval=10,
    showvalue=0,
    troughcolor="#69EAFF",
    fg="blue",
    bg="green"
    )
scale.set(67)
scale.place(x=1300,y=0)
button2 = Button(
    window,
    text="Scale Value",
    command=scalevalue
    )
button2.pack(side=RIGHT)

# List box
def listvalue():
    print(listbox.get(listbox.curselection()))

listbox=Listbox(
    window,
    bg="#f7ffde"
    )
listbox.pack()
listbox.insert(1,option[0])
listbox.insert(2,option[1])
listbox.insert(3,option[2])
listsubmit = Button(
    window,
    text="List",
    command=listvalue
    )
listsubmit.pack()

# Message Box
def popbox():
    messagebox.showinfo(
        title="Bugggggg",
        message="Heheheheh"
    )
    # messagebox.showwarning()
    if messagebox.askyesno(
        title="Yes or no",
        message="Yes or No :)"
    ):
        print("Press Yes")
    else:
        print("Press No")
    # messagebox.askokcancel()
    # messagebox.askokcancel()
    # messagebox.askquestion()
    # messagebox.askretrycancel()
    # messagebox.askyesnocancel()

button3 = Button(
    window,
    text="Pop Up",
    command=popbox
)
button3.pack()

# Text ( can input)
def submit2():
    input = text.get(1.0,END)
    print(input)

v1 = StringVar()
text = Text(
    window,
    bg="light yellow"
)
text.pack()
button4 = Button(
    window,
    text="Text submit",
    command=submit2
)
button4.pack()

# Tkinter filedialog
# def openfile():
#     filepath = filedialog.askopenfilename()
#     """
#     In Windows:
#         filedialog.askopenfilename(
#             initialdir="C:\\Users\\username\\",
#             title="Open a File",
#             filetypes=(
#             ("text files",".txt"),
#             ("all files,".*")
#             )
#         )

#     """
#     file = open(filepath)
#     print(file.read())
#     file.close()

# def savefile():
#     file = filedialog.asksaveasfile()
#     filetext = str(text.get(1.0,END))
#     file.write(v1)
#     file.close()

# savefile()

# Mulitple Checkbutton
opts = ["Option A", "Option B", "Option C"]
vars = [BooleanVar(value=False) for _ in opts]

for text, v in zip(opts, vars):
    cb = tk.Checkbutton(root, text=text, variable=v)
    cb.pack(anchor="w")

window.mainloop()