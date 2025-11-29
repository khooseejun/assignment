from tkinter import *
from tkinter import messagebox
from datetime import date, timedelta, datetime

class BaseGoalPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages 
        self.career_choices = []
        
        top = Frame(self, bg="#CFE8FF")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Goal Tracker", font=("Arial", 20, "bold"),bg="#CFE8FF").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", fg="white",height=1, width=10).pack(side="right", padx=12)

        goals_body = Frame(self, bd=1, relief="raised")
        goals_body.pack(fill="both", expand=True, padx=15, pady=5)
        goals_body.pack_propagate(False)

        def show_career_details(*args):
            career = selected_career.get()
            if career in career_details:
                info = career_details[career]
                output_label.config(
                    text=f"{career}\n\n"
                        f"Short-term:\n{info['short_term']}\n\n"
                        f"Long-term:\n{info['long_term']}"
                )
            else:
                output_label.config(text="Choose a career")
        
        def popbox():
            career = selected_career.get()
            if career not in career_list:
                messagebox.showwarning(title="Career Submit",message="Choose a career, not choose a bug! :(")
                return
            if career in self.career_choices:
                messagebox.showwarning(title="Career Submit", message="You already choose this career before.")
                return
            
            if messagebox.askokcancel(title="Career Submit",message=f"Are you sure you want choose {career} ?"):
                self.save_career_choice(career)
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

        output_label = Label(goals_body, text="", justify=LEFT,font=("Arial", 12, "bold"),anchor="w")
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
        
        self.load_career_choices()
    
    def load_career_choices(self):
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
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
        """Generate weekly tasks for the selected career and save them to tasks.txt."""
        today = date.today()
        
        with open("tasks.txt", "a") as f:
            for day_num in range(1, 8):
                if day_num in self.career_task[career]:
                    task_info = self.career_task[career][day_num]
                    title = list(task_info.keys())[0]
                    description = list(task_info.values())[0]
                    
                    task_date = today + timedelta(days=day_num - 1)
                    
                    # New format: TASK|description|date|completed|career|day_of_week|is_career_task|created_date
                    task_line = (
                        f"TASK|{title}: {description}|{task_date.strftime('%Y-%m-%d')}|False|"
                        f"{career}|{day_num}|True|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    f.write(task_line)