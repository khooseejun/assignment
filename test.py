from tkinter import *

window = Tk()
window.title("Python Tkinter Windows")
window.geometry("1080x920")
window.resizable(False,False)
window.config(background="#0C090A")

on_or_off = IntVar()
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
    )
    radiobutton.pack()


window.mainloop()