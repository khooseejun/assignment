from tkinter import *

class BasePlannerPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages
        top = Frame(self, bg="#7FB7FF")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Daily Task Planner", font=("Arial", 20, "bold"),bg="#7FB7FF").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", fg="white",height=1, width=10).pack(side="right", padx=12)

        planner_frame = Frame(self, bd=1, relief="raised")
        planner_frame.pack(fill="both", expand=True, padx=12, pady=8)
        Label(planner_frame, text="planner_frame function write here", font=("Arial", 15, "bold")).pack(anchor="center", expand=True)