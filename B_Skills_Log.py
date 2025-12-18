from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

# ============================================================
# BaseSkillsLogPage
# Purpose:
# - Allow user to record completed courses, skills, and certifications
# - Display all records in a Treeview table
# - Save records into a text file for persistence
# ============================================================

class BaseSkillsLogPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages  # Reference to main app for navigation
 
        # ------------------------------
        # Generate year list (2000 to 5 years ahead)
        # ------------------------------
        current_year = datetime.now().year
        self.year_values = [str(y) for y in range(2000, current_year + 6)]

        # ------------------------------
        # Top Header Bar
        # ------------------------------
        top = Frame(self, bg="#3F85F5")
        top.pack(fill="x", pady=8, padx=10)

        Label(top, text="Skills & Certifications Log",font=("Arial", 20, "bold"),bg="#3F85F5").pack(side="left", padx=12)
        Button(top, text="Back", bg="red", fg="white",width=10, command=self.go_back).pack(side="right", padx=12)

        main = Frame(self)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # ----------------------------
        # LEFT PANEL: Input Forms
        # -----------------------------
        left = Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # ------------------------------
        # Course Recording Section
        # ------------------------------
        courses_box = LabelFrame(left, text="Record Completed Courses",font=("Arial", 12, "bold"),padx=10, pady=10, bg="#A8C7F1",fg="#1100FC")
        courses_box.pack(fill="x", pady=10)
        
        # Course name input
        Label(courses_box, text="Course Name:",bg="#A8C7F1").grid(row=0, column=0, sticky="w")
        self.course_name = Entry(courses_box, width=30)
        self.course_name.grid(row=0, column=1)
        
        # ------------------------------
        # Start Date Selection
        # ------------------------------
        Label(courses_box, text="Start Date:", bg="#A8C7F1",).grid(row=1, column=0, sticky="w")
        start_frame = Frame(courses_box)
        start_frame.grid(row=1, column=1, sticky="w")

        self.start_day = ttk.Combobox(start_frame, width=3, values=[str(i).zfill(2) for i in range(1, 32)], state="readonly")
        self.start_day.set(datetime.now().strftime("%d"))
        self.start_day.pack(side=LEFT)

        Label(start_frame, text="/",bg="#A8C7F1").pack(side=LEFT)

        self.start_month = ttk.Combobox(start_frame, width=3,values=[str(i).zfill(2) for i in range(1, 13)],  state="readonly")
        self.start_month.set(datetime.now().strftime("%m"))
        self.start_month.pack(side=LEFT)

        Label(start_frame, text="/",bg="#A8C7F1").pack(side=LEFT)

        self.start_year = ttk.Combobox(start_frame, width=6,   values=self.year_values, state="readonly")
        self.start_year.set(str(current_year))
        self.start_year.pack(side=LEFT)
        
        # ------------------------------
        # Completion Date Selection
        # ------------------------------
        Label(courses_box, text="Completion Date:",bg="#A8C7F1").grid(row=2, column=0, sticky="w")
        end_frame = Frame(courses_box)
        end_frame.grid(row=2, column=1, sticky="w")

        self.end_day = ttk.Combobox(end_frame, width=3,values=[str(i).zfill(2) for i in range(1, 32)], state="readonly")
        self.end_day.set(datetime.now().strftime("%d"))
        self.end_day.pack(side=LEFT)

        Label(end_frame, text="/",bg="#A8C7F1").pack(side=LEFT)

        self.end_month = ttk.Combobox(end_frame, width=3, values=[str(i).zfill(2) for i in range(1, 13)], state="readonly")
        self.end_month.set(datetime.now().strftime("%m"))
        self.end_month.pack(side=LEFT)

        Label(end_frame, text="/",bg="#A8C7F1").pack(side=LEFT)

        self.end_year = ttk.Combobox(end_frame, width=6,values=self.year_values, state="readonly")
        self.end_year.set(str(current_year))
        self.end_year.pack(side=LEFT)

        Label(courses_box, text="Priority:",bg="#A8C7F1").grid(row=3, column=0, sticky="w")
        self.priority = StringVar(value="Medium")
        OptionMenu(courses_box, self.priority, "High", "Medium", "Low").grid(row=3, column=1, sticky="w")

        Button(courses_box, text="Add Course", bg="green", width=20, command=self.add_course).grid(row=4, column=0, columnspan=2, pady=10)

        # ===== SKILLS =====
        skills_box = LabelFrame(left, text="Add Skill",  font=("Arial", 12, "bold"),  padx=10, pady=10,bg="#A8C7F1")
        skills_box.pack(fill="x", pady=10)

        Label(skills_box, text="Skill Name:",bg="#A8C7F1").grid(row=0, column=0, sticky="w")
        self.skill_name = Entry(skills_box, width=30)
        self.skill_name.grid(row=0, column=1)

        Button(skills_box, text="Add Skill", bg="green",width=20, command=self.add_skill).grid(row=1, column=0, columnspan=2, pady=10)

        # ===== CERTIFICATIONS =====
        cert_box = LabelFrame(left, text="Add Certification", font=("Arial", 12, "bold",), padx=10, pady=10,bg="#A8C7F1")
        cert_box.pack(fill="x", pady=10)

        Label(cert_box, text="Certification:",bg="#A8C7F1").grid(row=0, column=0, sticky="w")
        self.cert_name = Entry(cert_box, width=30)
        self.cert_name.grid(row=0, column=1)

        Label(cert_box, text="Issued by:",bg="#A8C7F1").grid(row=1, column=0, sticky="w")
        self.cert_issuer = Entry(cert_box, width=30)
        self.cert_issuer.grid(row=1, column=1)

        Label(cert_box, text="Date Awarded:",bg="#A8C7F1").grid(row=2, column=0, sticky="w")
        award_frame = Frame(cert_box)
        award_frame.grid(row=2, column=1, sticky="w")

        self.award_day = ttk.Combobox(award_frame, width=3,values=[str(i).zfill(2) for i in range(1, 32)],state="readonly")
        self.award_day.set(datetime.now().strftime("%d"))
        self.award_day.pack(side=LEFT)

        Label(award_frame, text="/",bg="#A8C7F1").pack(side=LEFT)

        self.award_month = ttk.Combobox(award_frame, width=3,values=[str(i).zfill(2) for i in range(1, 13)], state="readonly")
        self.award_month.set(datetime.now().strftime("%m"))
        self.award_month.pack(side=LEFT)

        Label(award_frame, text="/",bg="#A8C7F1").pack(side=LEFT)

        self.award_year = ttk.Combobox(award_frame, width=6, values=self.year_values, state="readonly")
        self.award_year.set(str(current_year))
        self.award_year.pack(side=LEFT)

        Button(cert_box, text="Add Certification", bg="green", width=20, command=self.add_certification).grid(row=3, column=0, columnspan=2, pady=10)

        # RIGHT Panel: Display Table
        right = Frame(main)
        right.pack(side="right", fill="both", expand=True)
        
        Label(right, text="Your Courses, Skills & Certifications",font=("Arial", 14, "bold")).pack(pady=5)
        
        delete_frame = Frame(right)
        delete_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        Button(delete_frame, text="Delete Selected",bg="red", fg="white", width=15, command=self.delete_selected).pack(side="left")
        # Treeview to display records
        columns = ("Type", "Name", "Details")
        self.tree = ttk.Treeview(right, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill=BOTH, expand=True, padx=10)

    # ===== HELPER METHODS =====
    def get_date_string(self, d, m, y):
        try:
            datetime.strptime(f"{d.get()}/{m.get()}/{y.get()}", "%d/%m/%Y")
            return f"{d.get()}/{m.get()}/{y.get()}"
        except:
            return None

    def append_to_file(self, text):
        with open("skills_log.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

    # Add Record Functions
    def add_course(self):
        start = self.get_date_string(self.start_day, self.start_month, self.start_year)
        end = self.get_date_string(self.end_day, self.end_month, self.end_year)

        if not self.course_name.get().strip() or not start or not end:
            messagebox.showerror("Error", "Invalid input")
            return

        line = f"[Course] {self.course_name.get()} | Start: {start} | End: {end} | Priority: {self.priority.get()}"
        self.tree.insert("", END, values=("Course", self.course_name.get(), line))
        self.append_to_file(line)
        self.course_name.delete(0, END)

    def add_skill(self):
        if self.skill_name.get().strip():
            line = f"[Skill] {self.skill_name.get()}"
            self.tree.insert("", END, values=("Skill", self.skill_name.get(), ""))
            self.append_to_file(line)
            self.skill_name.delete(0, END)
        else:
         messagebox.showerror("Error", "Please enter a skill name")

    def add_certification(self):
        award_date = self.get_date_string(self.award_day, self.award_month, self.award_year)

        if not self.cert_name.get().strip() or not self.cert_issuer.get().strip() or not award_date:
            messagebox.showerror("Error", "Invalid input")
            return

        line = f"[Certification] {self.cert_name.get()} | Issued by: {self.cert_issuer.get()} | Date Awarded: {award_date}"
        self.tree.insert("", END, values=("Certification", self.cert_name.get(), line))
        self.append_to_file(line)
        self.cert_name.delete(0, END)
        self.cert_issuer.delete(0, END)
    
    def delete_selected(self):
        selected_items = self.tree.selection()
        
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an item to delete")
            return
        confirm = messagebox.askyesno("Confirm Delete",  "Are you sure you want to delete the selected item(s)?" )
        if not confirm:
            return
        for item in selected_items:
            self.tree.delete(item)
    #Navigation
    def go_back(self):
        self.pages.show_frame("HomePage")