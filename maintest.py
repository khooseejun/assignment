from tkinter import *
from tkinter import messagebox, ttk
from pathlib import Path
from datetime import datetime, date, timedelta
# import json >:(

class BasePage(Frame):
    # All pages inherit from this base for convenience
    def __init__(self, parent, pages):
        super().__init__(parent)
        # store reference to the "pages" controller (previously named controller)
        self.pages = pages

class MainMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("1024x768")
        container = Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # home_frame = HomePage(parent=container, pages=self)
        # self.frames["HomePage"] = home_frame
        # home_frame.grid(row=0, column=0, sticky="nsew")

        # goal_frame = GoalPage(parent=container, pages=self)
        # self.frames["GoalPage"] = goal_frame
        # goal_frame.grid(row=0, column=0, sticky="nsew")

        # skills_frame = SkillsLogPage(parent=container, pages=self)
        # self.frames["SkillsLogPage"] = skills_frame
        # skills_frame.grid(row=0, column=0, sticky="nsew")

        # planner_frame = PlannerPage(parent=container, pages=self)
        # self.frames["PlannerPage"] = planner_frame
        # planner_frame.grid(row=0, column=0, sticky="nsew")

        # achievement_frame = AchievementPage(parent=container, pages=self)
        # self.frames["AchievementPage"] = achievement_frame
        # achievement_frame.grid(row=0, column=0, sticky="nsew")
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
    
    def txtfilefunc():
        try:
            with open("tasks.txt",'r') as thetxtfile:
                content = thetxtfile.read()
                thetxtfile.close()
            print("Text file exist and valid")
        except FileNotFoundError:
            txtfile_write = open("tasks.txt", "x")
            txtfile_write.write("")
            txtfile_write.close()

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
        self.career_choices = []
        
        top = Frame(self)
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Goal Tracker", font=("Arial", 20, "bold")).pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", fg="white",height=1, width=10).pack(side="right", padx=12)

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
                return
            elif career in self.career_choices:
                messagebox.showwarning(title="Career Submit", message="You already choose this career before.")
                return
            
            if messagebox.askokcancel(title="Career Submit",message=f"Are you sure you want choose {career} ?"):
                # Save to tasks.txt
                self.save_career_choice(career)
                # Generate tasks for this career
                self.generate_career_tasks(career)
                
                messagebox.showinfo(title="Career Submit", 
                    message=f"Career '{career}' selected successfully!\n\n"
                           f"7 daily tasks have been added to your Daily Task Planner.\n"
                           f"Check the Planner page to see your new tasks!")
            
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

        output_label = Label(goals_body, text={"",""}, justify=LEFT,font=("Arial", 12, "bold"),anchor="w")
        output_label.pack(padx=10, pady=20, fill="both")
        output_label.config(text="Choose a career")

        submit = Button(goals_body, text="Submit", bg="blue", fg="white",width=30, height=2,command=popbox)
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
        
        # Store career tasks as instance variable - FIXED: Using proper dictionary format
        self.career_task = {
            "Full-Stack Developer": {
                1: {"Front-End Focus": "Work on a single HTML/CSS component (e.g., a navbar, a card). Make it pixel-perfect and responsive."},
                2: {"Back-End Focus": "Build a simple REST API endpoint in Flask (e.g., /api/tasks that returns a list of tasks)."},
                3: {"Integration": "Use JavaScript in your front-end to fetch data from your Flask API and display it dynamically on your HTML page."},
                4: {"Database Day": "Write a SQL query or use an ORM to add, read, update, or delete a record from your database."},
                5: {"Debugging & Polish": "Spend time fixing a known bug, improving code structure, or writing a simple test."},
                6: {"Learning & Exploration": "Watch a tutorial or read documentation about a concept you struggled with during the week (e.g., authentication, a CSS framework)."},
                7: {"Project & Deployment": "Work on a larger feature for your blog. Research one aspect of deployment (e.g., setting up a server, using Docker)."}
            },
            "Machine Learning Engineer": {
                1: {"Data Wrangling": "Clean, explore, and preprocess a dataset. Practice using pandas and visualization libraries."},
                2: {"Model Building": "Implement a machine learning model from scratch (using scikit-learn or TensorFlow/PyTorch) on a clean dataset."},
                3: {"Theory & Math": "Spend 30-60 minutes studying the mathematical fundamentals behind a specific algorithm (e.g., how gradient descent works, what loss functions are)."},
                4: {"Evaluation & Metrics": "Evaluate your model from Day 2. Calculate different metrics (accuracy, precision, recall, F1-score) and analyze where it failed."},
                5: {"Kaggle/Competition": "Actively participate in a Kaggle competition. This could be reading discussions, experimenting with new features, or trying a different model architecture."},
                6: {"Deep Learning": "Build and train a simple neural network, even if it's for a toy problem like MNIST digit classification."},
                7: {"Pipeline & MLOps": "Work on automating part of your workflow. Write a script to automatically preprocess data or look into tools like MLflow for experiment tracking."}
            },
            "Site Reliability Engineer": {
                1: {"Infrastructure as Code": "Write or modify a Terraform/CloudFormation script to define a piece of infrastructure (e.g., an S3 bucket, a VM)."},
                2: {"CI/CD Pipeline": "Work on a Jenkinsfile, GitHub Action, or GitLab CI configuration. Automate one step, like running tests or building a Docker image."},
                3: {"Containers & Orchestration": "Write a Dockerfile for a simple application or practice a kubectl command to manage Kubernetes pods."},
                4: {"Monitoring & Logging": "Set up a dashboard in Prometheus/Grafana or write a query in Splunk/ELK to analyze application logs."},
                5: {"Scripting & Automation": "Write a Bash or Python script to automate a repetitive system administration task (e.g., log rotation, health checks)."},
                6: {"Networking & Security": "Study a networking concept (e.g., TCP/IP, DNS, load balancers) or a security best practice (e.g., least privilege)."},
                7: {"Chaos Engineering & Post-Mortem": "Intentionally break something in a test environment and practice documenting the incident and recovery steps."}
            },
            "Mobile Development Specialist": {
                1: {"UI Construction": "Build a single screen in your app using SwiftUI, focusing on layout and basic user interaction."},
                2: {"Data & Logic": "Implement the data model and business logic for a feature (e.g., how to save a user's note, how to calculate a result)."},
                3: {"Navigation & Flow": "Work on app navigation, making sure screens connect properly and pass data between them."},
                4: {"API Integration": "Write network code to fetch data from a public API and display it in your app."},
                5: {"Platform Features": "Integrate a native iOS feature (e.g., Camera, Location Services, Notifications) into your app."},
                6: {"Performance & Debugging": "Profile your app for memory leaks or performance bottlenecks. Fix a bug or improve an animation."},
                7: {"App Store Prep": "Work on assets for the App Store (screenshots, description) or research the app review guidelines and provisioning profiles."}
            },
            "Cybersecurity Engineer": {
                1: {"Active Exploitation": "Work on an OSCP-like challenge box (from HTB, TryHackMe, or VulnHub). Focus on enumeration and initial access."},
                2: {"Privilege Escalation": "Practice privilege escalation techniques on the box from Day 1, either on Linux or Windows."},
                3: {"Defensive Security": "Analyze a sample of malicious code or network traffic (e.g., using Wireshark) to identify Indicators of Compromise (IOCs)."},
                4: {"Tool Proficiency": "Master a specific tool (e.g., nmap, Burp Suite, Metasploit). Learn one new switch or feature in depth."},
                5: {"Scripting for Security": "Write a small Python script to automate a penetration testing task (e.g., a custom fuzzer, a password cracker)."},
                6: {"Theory & Protocols": "Study the inner workings of a network protocol (e.g., TCP handshake, DNS, HTTP/S) or a common vulnerability class (e.g., SQLi, XSS)."},
                7: {"Documentation": "Write a detailed penetration test report for a machine you compromised during the week."}
            },
            "Data Engineer": {
                1: {"Data Ingestion": "Write a script to extract data from a source (e.g., a public API, a CSV file, a database) and land it in a staging area."},
                2: {"Data Transformation": "Write a SQL query or a PySpark script to clean, filter, and aggregate the data you ingested."},
                3: {"Data Orchestration": "Define or modify a task in an orchestration tool like Apache Airflow. Set up dependencies between tasks."},
                4: {"Data Warehousing": "Design a star or snowflake schema for a business problem. Practice writing efficient analytical queries against it."},
                5: {"Cloud & Distributed Systems": "Complete a tutorial or work with a specific cloud data service (e.g., AWS Glue, Google BigQuery, Azure Data Factory)."},
                6: {"Performance Tuning": "Analyze a slow-running query or job and try to optimize it (e.g., by adding an index, partitioning data, changing the execution plan)."},
                7: {"Monitoring & Quality": "Implement a data quality check (e.g., ensuring a column has no nulls, that counts are within expected ranges)."}
            }
        }
        
        # Load existing career choices
        self.load_career_choices()
    
    def load_career_choices(self):
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
                    # Parse the file to get career choices
                    lines = content.strip().split('\n')
                    for line in lines:
                        if line.startswith("CAREER:"):
                            career = line[7:].strip()
                            if career and career not in self.career_choices:
                                self.career_choices.append(career)
        except FileNotFoundError:
            self.career_choices = []
    
    def save_career_choice(self, career):
        try:
            with open("tasks.txt", "a") as f:
                f.write(f"CAREER:{career}\n")
                if career not in self.career_choices:
                    self.career_choices.append(career)
        except FileNotFoundError:
            with open("tasks.txt", "w") as f:
                f.write(f"CAREER:{career}\n")
                self.career_choices.append(career)
    
    def generate_career_tasks(self, career):
        # Generate weekly tasks for the selected career
        # Get the current highest task ID
        max_id = 0
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
                    lines = content.strip().split('\n')
                    for line in lines:
                        if line.startswith("TASK:"):
                            parts = line[5:].split('|')
                            if len(parts) >= 1:
                                try:
                                    task_id = int(parts[0])
                                    if task_id > max_id:
                                        max_id = task_id
                                except ValueError:
                                    pass
        except FileNotFoundError:
            pass
        
        # Generate tasks for the next 7 days starting from today
        today = date.today()
        
        for day_num in range(1, 8):
            if day_num in self.career_task[career]:
                task_info = self.career_task[career][day_num]
                # FIXED: Now task_info is a proper dictionary
                title = list(task_info.keys())[0]
                description = list(task_info.values())[0]
                
                # Calculate the date for this day of the week
                task_date = today + timedelta(days=day_num - 1)
                
                # Format: TASK:id|description|date|completed|career|day_of_week|is_career_task|created_date
                task_line = f"TASK:{max_id + day_num}|{title}: {description}|{task_date.strftime('%Y-%m-%d')}|False|{career}|{day_num}|True|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                with open("tasks.txt", "a") as f:
                    f.write(task_line)

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
        self.career_choices = []
        self.current_date_filter = "all"
        self.current_career_filter = "All Careers"
        
        top = Frame(self,bg="#FFFDFA")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Daily Task Planner", font=("Arial", 20, "bold"),bg="#FFFDFA").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        # Main container
        main_container = Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # REMOVED: Left side - Add task form
        # This entire section has been removed as requested
        
        # Right side - Task list
        right_frame = Frame(main_container, bd=1, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True)
        
        Label(right_frame, text="Task List", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Filter buttons
        filter_frame = Frame(right_frame)
        filter_frame.pack(pady=10)
        
        Label(filter_frame, text="Filter by Date:").pack()
        
        date_button_frame = Frame(filter_frame)
        date_button_frame.pack(pady=5)
        
        Button(date_button_frame, text="All", command=lambda: self.apply_filters("all", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="Today", command=lambda: self.apply_filters("today", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="Tomorrow", command=lambda: self.apply_filters("tomorrow", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="This Week", command=lambda: self.apply_filters("week", self.current_career_filter), width=10).pack(side="left", padx=2)
        
        # Career filter
        career_frame = Frame(right_frame)
        career_frame.pack(pady=10)
        
        Label(career_frame, text="Filter by Career:").pack()
        
        self.career_filter_var = StringVar()
        self.career_filter_var.set("All Careers")
        self.career_filter_menu = OptionMenu(career_frame, self.career_filter_var, "All Careers", command=lambda x: self.apply_filters(self.current_date_filter, self.career_filter_var.get()))
        self.career_filter_menu.pack(pady=5)
        
        # Task statistics
        stats_frame = Frame(right_frame)
        stats_frame.pack(pady=10)
        
        self.stats_label = Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        # Task list frame with scrollbar
        list_frame = Frame(right_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Task listbox
        self.task_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode="single")
        self.task_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Task control buttons
        control_frame = Frame(right_frame)
        control_frame.pack(pady=10)
        
        Button(control_frame, text="Mark Complete", command=self.mark_complete, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        Button(control_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white").pack(side="left", padx=5)
        
        # Load tasks from text file
        self.load_tasks()
    
    def on_show(self):
        # Refresh tasks when page is shown
        self.load_tasks()
        self.load_career_choices()
        self.update_career_filter()
        self.apply_filters("all", "All Careers")
        self.update_statistics()
    
    def load_career_choices(self):
        """Load career choices from text file"""
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
                    # Parse the file to get career choices
                    lines = content.strip().split('\n')
                    for line in lines:
                        if line.startswith("CAREER:"):
                            career = line[7:].strip()
                            if career and career not in self.career_choices:
                                self.career_choices.append(career)
        except FileNotFoundError:
            self.career_choices = []
    
    def update_career_filter(self):
        """Update the career filter dropdown menu"""
        menu = self.career_filter_menu["menu"]
        menu.delete(0, "end")
        
        menu.add_command(label="All Careers", command=lambda: self.apply_filters(self.current_date_filter, "All Careers"))
        for career in self.career_choices:
            menu.add_command(label=career, command=lambda c=career: self.apply_filters(self.current_date_filter, c))
    
    def apply_filters(self, date_filter, career_filter):
        """Apply both date and career filters"""
        self.current_date_filter = date_filter
        self.current_career_filter = career_filter
        
        # Update the career filter variable to match
        self.career_filter_var.set(career_filter)
        
        today = date.today()
        tomorrow = today + timedelta(days=1)
        week_end = today + timedelta(days=7)
        
        # First filter by date
        if date_filter == "all":
            date_filtered = self.tasks
        elif date_filter == "today":
            date_filtered = [task for task in self.tasks 
                           if datetime.strptime(task["date"], "%Y-%m-%d").date() == today]
        elif date_filter == "tomorrow":
            date_filtered = [task for task in self.tasks 
                           if datetime.strptime(task["date"], "%Y-%m-%d").date() == tomorrow]
        elif date_filter == "week":
            date_filtered = [task for task in self.tasks 
                           if today <= datetime.strptime(task["date"], "%Y-%m-%d").date() <= week_end]
        else:
            date_filtered = self.tasks
        
        # Then filter by career if selected
        if career_filter != "All Careers":
            self.filtered_tasks = [task for task in date_filtered if task.get("career") == career_filter]
        else:
            self.filtered_tasks = date_filtered
        
        self.update_task_list()
        self.update_statistics()
    
    def update_statistics(self):
        """Update task statistics display"""
        total_tasks = len(self.filtered_tasks)
        completed_tasks = sum(1 for task in self.filtered_tasks if task.get("completed", False))
        career_tasks = sum(1 for task in self.filtered_tasks if task.get("is_career_task", False))
        
        stats_text = f"Total: {total_tasks} | Completed: {completed_tasks} | Career Tasks: {career_tasks}"
        self.stats_label.config(text=stats_text)
    
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
                    lines = content.strip().split('\n')
                    self.tasks = []
                    for line in lines:
                        if line.startswith("TASK:"):
                            parts = line[5:].split('|')
                            if len(parts) >= 8:
                                self.tasks.append({
                                    "id": int(parts[0]),
                                    "description": parts[1],
                                    "date": parts[2],
                                    "completed": parts[3].lower() == "true",
                                    "career": parts[4] if parts[4] != "None" else None,
                                    "day_of_week": int(parts[5]) if parts[5] != "None" else None,
                                    "is_career_task": parts[6].lower() == "true",
                                    "created_date": parts[7]
                                })
                else:
                    self.tasks = []
        except FileNotFoundError:
            self.tasks = []
    
    def save_tasks(self):
        # First, read all existing content to preserve career choices
        career_lines = []
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
                    lines = content.strip().split('\n')
                    for line in lines:
                        if line.startswith("CAREER:"):
                            career_lines.append(line)
        except FileNotFoundError:
            career_lines = []
        
        # Write back career choices and updated tasks
        with open("tasks.txt", "w") as f:
            for line in career_lines:
                f.write(line + "\n")
            
            for task in self.tasks:
                # Format: TASK:id|description|date|completed|career|day_of_week|is_career_task|created_date
                f.write(f"TASK:{task['id']}|{task['description']}|{task['date']}|{task['completed']}|{task['career']}|{task['day_of_week']}|{task['is_career_task']}|{task['created_date']}\n")
    
    def update_task_list(self):
        self.task_listbox.delete(0, END)
        
        # Sort tasks by date and by career tasks first
        def sort_key(task):
            date_val = datetime.strptime(task["date"], "%Y-%m-%d")
            # Career tasks come first (is_career_task=True), then custom tasks
            return (not task.get("is_career_task", False), date_val)
        
        sorted_tasks = sorted(self.filtered_tasks, key=sort_key)
        
        for task in sorted_tasks:
            status = "✓" if task["completed"] else "○"
            career_tag = ""
            if task.get("is_career_task"):
                career_tag = f"[{task.get('career', 'Career')}] "
            
            display_text = f"{status} [{task['date']}] {career_tag}{task['description']}"
            self.task_listbox.insert(END, display_text)
    
    def mark_complete(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task")
            return
        
        # Find the task in the filtered list
        index = selection[0]
        if index < len(self.filtered_tasks):
            task_id = self.filtered_tasks[index]["id"]
            
            # Find and update the task in the main list
            for task in self.tasks:
                if task["id"] == task_id:
                    task["completed"] = not task["completed"]
                    break
            
            self.save_tasks()
            self.apply_filters(self.current_date_filter, self.current_career_filter)
    
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task")
            return
        
        # Find the task in the filtered list
        index = selection[0]
        if index < len(self.filtered_tasks):
            task_id = self.filtered_tasks[index]["id"]
            
            # Confirm deletion
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                # Remove the task from the main list
                self.tasks = [task for task in self.tasks if task["id"] != task_id]
                self.save_tasks()
                self.apply_filters(self.current_date_filter, self.current_career_filter)

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
    MainMenu.txtfilefunc()
    MainMenu().mainloop()