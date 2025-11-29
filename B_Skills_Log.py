from tkinter import *

class BaseSkillsLogPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages
        top = Frame(self, bg="#3F85F5")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Skills Log", font=("Arial", 20, "bold"),bg="#3F85F5").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", fg="white",height=1, width=10).pack(side="right", padx=12)

        skills_frame = Frame(self, bd=1, relief="raised")
        skills_frame.pack(fill="both", expand=True, padx=12, pady=8)
        Label(skills_frame, text="skills_frame function write here", font=("Arial", 15, "bold")).pack(anchor="center", expand=True)