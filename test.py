from tkinter import *

window = Tk()
window.title("Python Tkinter Windows")
window.geometry("1080x920")
window.resizable(False,False)
window.config(background="#0C090A")

on_or_off = IntVar()
radiostatus = IntVar()
option = ["Main", "Sub", "Settings"]

def click():
    print("Button Clicked")

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

def buttonstatus():
    if (on_or_off.get() == 1):
        print("Agree")
    else:
        print("Disagree :(")

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

def scalevalue():
    print(scale.get())

def listvalue():
    print(listbox.get(listbox.curselection()))

# Label
label = Label(
    window,text="Hello, World!",
    font=("Arial",24,"bold"),
    fg="green",
    bg="blue",
    padx=10,
    pady=10
)
label.pack()

# Button
button = Button(
    window,
    text="Click Me",
    command=click,
    fg="green",
    bg="blue",
    activebackground="white"
)
button.pack()

# Entry
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
thecheckbutton = Checkbutton(
    window,
    text="I agree the terms and condition.",
    variable=on_or_off,
    onvalue=1,
    offvalue=0,
    command=buttonstatus
)
thecheckbutton.pack()

# Radio Button ( same as check button, but only 1 active )
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
scale.pack()
button2 = Button(
    window,
    text="Scale Value",
    command=scalevalue
    )
button2.pack()

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

window.mainloop()