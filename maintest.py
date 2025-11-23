from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import json
import os

class BasePage(Frame):
    """ All pages inherit from this base for convenience """
    def __init__(self, parent, pages):
        super().__init__(parent)
        # store reference to the "pages" controller (previously named controller)
        self.pages = pages

class MainMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title("Main menu")
        self.geometry("1024x768")
        self.resizable(False,False)
        container = Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, GoalPage, SkillsLogPage, PlannerPage, AchievementPage):
            page_name = F.__name__
            # pass self as "pages" (previously passed as controller)
            frame = F(parent=container, pages=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        # Call an "on_show" method if present
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception:
                pass

class HomePage(BasePage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)
        header = Frame(self, height=100, bg="white", bd=2, relief="solid")
        header.pack(side="top", fill="x")
        header.pack_propagate(False)
        Label(header, text="LOGO", font=("Arial", 30, "bold")).pack(anchor="center", expand=True)

        move_text = Frame(self, bd=1, relief="raised")
        move_text.pack(fill="y")
        m_frame = Frame(move_text, bd=1, relief="raised")
        m_frame.pack(side="left", fill="y")
        self.m_canvas = Canvas(m_frame, width=400, height=50, bg="white", bd=1, relief="raised")
        self.m_canvas.pack(pady=15)
        self.m_text = self.m_canvas.create_text(
            0, 25, text="Welcome to use our application", font=("Arial", 13), anchor="w", tags="move_text")
        self.x = 0
        self.scroll_m_text()

        buttons_frame = Frame(self)
        buttons_frame.pack(padx=8)
        btn_opts = {"width": 30, "height": 2, "bd": 4, "relief": "raised"}
        Button(buttons_frame, text="Goal Tracker", command=lambda: self.pages.show_frame("GoalPage"), **btn_opts).pack(pady=15)
        Button(buttons_frame, text="Skills Log", command=lambda: self.pages.show_frame("SkillsLogPage"), **btn_opts).pack(pady=15)
        Button(buttons_frame, text="Daily Task Planner", command=lambda: self.pages.show_frame("PlannerPage"), **btn_opts).pack(pady=15)
        Button(buttons_frame, text="Achievement Summary", command=lambda: self.pages.show_frame("AchievementPage"), **btn_opts).pack(pady=15)
        Button(buttons_frame, text="Exit", command=self.pages.quit, **btn_opts).pack(pady=15)

    def scroll_m_text(self):
        width = 350
        dx = 1
        self.m_canvas.move("move_text", dx, 0)
        self.x += dx
        if self.x > width:
            self.x = 0
            self.m_canvas.delete("move_text")
            self.m_text = self.m_canvas.create_text(
                self.x, 25, text="Welcome to use our application",
                font=("Arial", 13), anchor="w", tags="move_text" )
        self.m_canvas.after(50, self.scroll_m_text)

class GoalPage(BasePage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)
        top = Frame(self)
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Goal Tracker", font=("Arial", 20, "bold")).pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        goals_body = Frame(self, bd=1, relief="raised")
        goals_body.pack(fill="both", expand=True, padx=15, pady=5)
        goals_body.pack_propagate(False)

        def show_career_details(*args):
            career = selected_career.get()  # get OptionMenu select
            info = career_details[career]

            # show short term and long term task below optionbox
            output_label.config(
                text=f"{career}\n\n"
                    f"Short-term:\n{info['short_term']}\n\n"
                    f"Long-term:\n{info['long_term']}"
            )

        def popbox():
            career = selected_career.get()
            if career not in career_list:
                messagebox.showwarning(title="Career Submit",message="Choose a career, not choose a bug! :(")
            elif messagebox.askokcancel(title="Career Submit",message=f"Are you sure you want choose {career} ?"):
                messagebox.showinfo(title="Career Submit", message="Task submit")
            
        weltext = Frame(goals_body,bd=2, relief="raised")
        weltext.pack(fill="x")

        Label(weltext, text="Let select your Career\nStart you target", font=("Arial", 20, "bold")).pack(padx=10)
        career_list = [
            "Full-Stack Developer",
            "Machine Learning Engineer",
            "Site Reliability Engineer",
            "Mobile Development Specialist",
            "Cybersecurity Engineer",
            "Data Engineer"
        ]

        selected_career = StringVar()
        selected_career.set("Choose a Career")
        
        OptionMenu(goals_body, selected_career, *career_list).pack(pady=10)
        selected_career.trace_add("write", show_career_details)

        next_btn = Button(goals_body, text="Next", command=show_career_details)
        next_btn.pack()

        output_label = Label(goals_body, text="", justify=LEFT,font=("Arial", 12, "bold"),anchor="w")
        output_label.pack(padx=10, pady=20, fill="both")

        submit = Button(goals_body, text="Submit", bg="blue",  width=30, height=2,command=popbox)
        submit.pack(side=BOTTOM,pady=10)

        career_details = {
            "Full-Stack Developer": {
                "short_term": "Build and deploy a simple personal blog project using HTML/CSS/JavaScript (Frontend) \nand Python/Flask (Backend) to a cloud server. (3 months)",
                "long_term": "Become a proficient full-stack developer capable of designing, building, and \ndeploying complex, data-driven web applications. (2 years)"
            },

            "Machine Learning Engineer": {
                "short_term": "Complete 3 end-to-end ML projects (e.g., predictive model, image classifier) and achieve a bronze medal \non a Kaggle competition. (6 months)",
                "long_term": "Transition into a professional AI/ML Engineer role, specializing in building and \ndeploying scalable machine learning models. (1.5 years)"
            },

            "Site Reliability Engineer": {
                "short_term": "Establish a complete CI/CD pipeline and achieve automated deployment & monitoring for a \nmicroservices project. (6 months)",
                "long_term": "Become a core SRE, improving system availability to 99.9% and establishing a robust incident \nresponse process. (2 years)"
            },

            "Mobile Development Specialist": {
                "short_term": "Independently develop and publish a fully-functional iOS app to the App Store. (4 months)",
                "long_term": "Master SwiftUI, Combine, and performance optimization to solve complex UI and \narchitectural challenges. (1.5 years)"
            },

            "Cybersecurity Engineer": {
                "short_term": "Obtain the OSCP certification and demonstrate the ability to independently find and exploit medium-to-high \nseverity vulnerabilities in authorized penetration tests. (1 year)",
                "long_term": "Specialize in AppSec or Threat Intelligence, capable of building proactive defense systems \nfor an enterprise. (3 years)"
            },

            "Data Engineer": {
                "short_term": "Design and build a scalable data pipeline that ingests, processes, and stores data from multiple sources \ninto a data warehouse. (8 months)",
                "long_term": "Become a lead data engineer, responsible for architecting and maintaining the company's \nentire data infrastructure. (2 years)"
            }
        }

class SkillsLogPage(BasePage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)
        top = Frame(self, bg="#18d8e6")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Skills Log", font=("Arial", 20, "bold")).pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        skills_frame = Frame(self, bd=1, relief="raised")
        skills_frame.pack(fill="both", expand=True, padx=12, pady=8)
        Label(skills_frame, text="skills_frame function write here", font=("Arial", 15, "bold")).pack(anchor="center", expand=True)

class PlannerPage(BasePage): # Daily Task Planner
    def __init__(self, parent, pages):
        super().__init__(parent, pages)
        self.tasks = []
        self.filtered_tasks = []
        self.data_file = "tasks.json"
        self.load_tasks()
        
        top = Frame(self,bg="#FFFDFA")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Daily Task Planner", font=("Arial", 20, "bold"),bg="#FFFDFA").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        # Main content frame
        main_frame = Frame(self, bd=1, relief="raised", bg="#FFFDFA")
        main_frame.pack(fill="both", expand=True, padx=12, pady=8)
        
        # Left side - Task input
        input_frame = Frame(main_frame, bg="#FFFDFA")
        input_frame.pack(side=LEFT, fill="both", expand=True, padx=10, pady=10)
        
        # Task input form
        form_frame = Frame(input_frame, bg="#FFFDFA", bd=1, relief="solid", padx=10, pady=10)
        form_frame.pack(fill="x", pady=(0, 10))
        
        Label(form_frame, text="Add New Task", font=("Arial", 16, "bold"), bg="#FFFDFA").pack(anchor="w", pady=(0, 10))
        
        # Task description
        Label(form_frame, text="Task Description:", font=("Arial", 12), bg="#FFFDFA").pack(anchor="w")
        self.task_desc = Entry(form_frame, font=("Arial", 12), width=30)
        self.task_desc.pack(fill="x", pady=(0, 10))
        
        # Date selection
        date_frame = Frame(form_frame, bg="#FFFDFA")
        date_frame.pack(fill="x", pady=(0, 10))
        
        Label(date_frame, text="Date:", font=("Arial", 12), bg="#FFFDFA").pack(side=LEFT)
        self.task_date = Entry(date_frame, font=("Arial", 12), width=12)
        self.task_date.pack(side=LEFT, padx=(5, 0))
        self.task_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        Button(date_frame, text="Today", command=self.set_today, bg="#e6f3ff", font=("Arial", 10)).pack(side=LEFT, padx=(10, 0))
        Button(date_frame, text="Tomorrow", command=self.set_tomorrow, bg="#e6f3ff", font=("Arial", 10)).pack(side=LEFT, padx=(5, 0))
        
        # Priority selection
        priority_frame = Frame(form_frame, bg="#FFFDFA")
        priority_frame.pack(fill="x", pady=(0, 10))
        
        Label(priority_frame, text="Priority:", font=("Arial", 12), bg="#FFFDFA").pack(side=LEFT)
        self.priority_var = StringVar(value="Medium")
        priorities = ["High", "Medium", "Low"]
        for priority in priorities:
            Radiobutton(priority_frame, text=priority, variable=self.priority_var, 
                       value=priority, bg="#FFFDFA", font=("Arial", 10)).pack(side=LEFT, padx=(10, 0))
        
        # Add task button
        Button(form_frame, text="Add Task", command=self.add_task, 
               bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=10)
        
        # Filter buttons
        filter_frame = Frame(input_frame, bg="#FFFDFA")
        filter_frame.pack(fill="x", pady=10)
        
        Label(filter_frame, text="Filter Tasks:", font=("Arial", 14, "bold"), bg="#FFFDFA").pack(anchor="w")
        
        filter_btn_frame = Frame(filter_frame, bg="#FFFDFA")
        filter_btn_frame.pack(fill="x", pady=5)
        
        Button(filter_btn_frame, text="All", command=lambda: self.filter_tasks("all"), 
               bg="#2196F3", fg="white", font=("Arial", 10), width=8).pack(side=LEFT, padx=(0, 5))
        Button(filter_btn_frame, text="Today", command=lambda: self.filter_tasks("today"), 
               bg="#FF9800", fg="white", font=("Arial", 10), width=8).pack(side=LEFT, padx=5)
        Button(filter_btn_frame, text="Tomorrow", command=lambda: self.filter_tasks("tomorrow"), 
               bg="#9C27B0", fg="white", font=("Arial", 10), width=8).pack(side=LEFT, padx=5)
        Button(filter_btn_frame, text="This Week", command=lambda: self.filter_tasks("week"), 
               bg="#607D8B", fg="white", font=("Arial", 10), width=8).pack(side=LEFT, padx=5)
        
        # Right side - Task list
        list_frame = Frame(main_frame, bg="#FFFDFA", bd=1, relief="solid")
        list_frame.pack(side=RIGHT, fill="both", expand=True, padx=(0, 10), pady=10)
        
        # Task list header
        list_header = Frame(list_frame, bg="#f0f0f0", height=40)
        list_header.pack(fill="x")
        list_header.pack_propagate(False)
        
        Label(list_header, text="Task List", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(anchor="center", expand=True)
        
        # Task list with scrollbar
        list_container = Frame(list_frame, bg="#FFFDFA")
        list_container.pack(fill="both", expand=True)
        
        self.task_canvas = Canvas(list_container, bg="#FFFDFA")
        scrollbar = Scrollbar(list_container, orient="vertical", command=self.task_canvas.yview)
        self.scrollable_frame = Frame(self.task_canvas, bg="#FFFDFA")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all"))
        )
        
        self.task_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.task_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.task_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Statistics
        stats_frame = Frame(list_frame, bg="#FFFDFA", height=40)
        stats_frame.pack(fill="x", side=BOTTOM)
        stats_frame.pack_propagate(False)
        
        self.stats_label = Label(stats_frame, text="Total: 0 | Completed: 0 | Pending: 0", 
                                font=("Arial", 10), bg="#FFFDFA")
        self.stats_label.pack(anchor="center", expand=True)
        
        # Load initial tasks
        self.filter_tasks("all")

    def set_today(self):
        self.task_date.delete(0, END)
        self.task_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def set_tomorrow(self):
        tomorrow = datetime.now() + timedelta(days=1)
        self.task_date.delete(0, END)
        self.task_date.insert(0, tomorrow.strftime("%Y-%m-%d"))

    def add_task(self):
        description = self.task_desc.get().strip()
        date_str = self.task_date.get().strip()
        priority = self.priority_var.get()
        
        if not description:
            messagebox.showwarning("Input Error", "Please enter a task description")
            return
            
        if not date_str:
            messagebox.showwarning("Input Error", "Please enter a date")
            return
            
        # Validate date format
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter date in YYYY-MM-DD format")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "date": date_str,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.task_desc.delete(0, END)
        self.filter_tasks("all")

    def toggle_task(self, task_id, var):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = var.get()
                break
        self.save_tasks()
        self.update_display()

    def delete_task(self, task_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.tasks = [task for task in self.tasks if task["id"] != task_id]
            self.save_tasks()
            self.filter_tasks("all")

    def filter_tasks(self, filter_type):
        today = datetime.now().date()
        
        if filter_type == "today":
            self.filtered_tasks = [task for task in self.tasks 
                                 if task["date"] == today.strftime("%Y-%m-%d")]
        elif filter_type == "tomorrow":
            tomorrow = today + timedelta(days=1)
            self.filtered_tasks = [task for task in self.tasks 
                                 if task["date"] == tomorrow.strftime("%Y-%m-%d")]
        elif filter_type == "week":
            end_of_week = today + timedelta(days=(6 - today.weekday()))
            self.filtered_tasks = [task for task in self.tasks 
                                 if datetime.strptime(task["date"], "%Y-%m-%d").date() <= end_of_week]
        else:  # "all"
            self.filtered_tasks = self.tasks.copy()
            
        # Sort by date and priority
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        self.filtered_tasks.sort(key=lambda x: (
            x["date"], 
            priority_order[x["priority"]],
            x["id"]
        ))
        
        self.update_display()

    def update_display(self):
        # Clear current display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Display tasks
        for task in self.filtered_tasks:
            task_frame = Frame(self.scrollable_frame, bg="#f9f9f9", bd=1, relief="solid", padx=10, pady=8)
            task_frame.pack(fill="x", padx=5, pady=2)
            
            # Checkbox for completion
            var = BooleanVar(value=task["completed"])
            checkbox = Checkbutton(task_frame, variable=var, bg="#f9f9f9",
                                 command=lambda t=task["id"], v=var: self.toggle_task(t, v))
            checkbox.pack(side=LEFT, padx=(0, 10))
            
            # Task info
            info_frame = Frame(task_frame, bg="#f9f9f9")
            info_frame.pack(side=LEFT, fill="x", expand=True)
            
            # Description with strikethrough if completed
            desc_text = task["description"]
            if task["completed"]:
                desc_text = f"✓ {desc_text}"
                desc_label = Label(info_frame, text=desc_text, font=("Arial", 11, "overstrike"), 
                                 bg="#f9f9f9", fg="gray", anchor="w")
            else:
                desc_label = Label(info_frame, text=desc_text, font=("Arial", 11, "bold"), 
                                 bg="#f9f9f9", anchor="w")
            desc_label.pack(fill="x")
            
            # Metadata
            meta_frame = Frame(info_frame, bg="#f9f9f9")
            meta_frame.pack(fill="x")
            
            # Priority with color coding
            priority_colors = {"High": "#ff4444", "Medium": "#ffaa00", "Low": "#44aa44"}
            priority_label = Label(meta_frame, text=task["priority"], 
                                 font=("Arial", 8, "bold"), 
                                 fg="white", bg=priority_colors[task["priority"]])
            priority_label.pack(side=LEFT, padx=(0, 10))
            
            # Date
            date_label = Label(meta_frame, text=task["date"], font=("Arial", 9), bg="#f9f9f9")
            date_label.pack(side=LEFT, padx=(0, 10))
            
            # Delete button
            delete_btn = Button(task_frame, text="×", font=("Arial", 12, "bold"), 
                              fg="red", bg="#f9f9f9", bd=0,
                              command=lambda t=task["id"]: self.delete_task(t))
            delete_btn.pack(side=RIGHT)
        
        # Update statistics
        total = len(self.filtered_tasks)
        completed = sum(1 for task in self.filtered_tasks if task["completed"])
        pending = total - completed
        
        self.stats_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {pending}")

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def on_show(self):
        # Refresh tasks when page is shown
        self.filter_tasks("all")

class AchievementPage(BasePage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)
        top = Frame(self)
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Achievement Summary", font=("Arial", 18, "bold")).pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        achievement_frame = Frame(self, bd=1, relief="raised")
        achievement_frame.pack(fill="both", expand=True, padx=12, pady=8)
        Label(achievement_frame, text="achievement_frame function write here", font=("Arial", 15, "bold")).pack(anchor="center", expand=True)

if __name__ == "__main__":
    MainMenu().mainloop()