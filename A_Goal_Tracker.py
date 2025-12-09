# A_Goal_Tracker.py
from tkinter import *
from tkinter import messagebox
from datetime import date, timedelta, datetime

class BaseGoalPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages 
        self.career_choices = []
        
        # Define career tasks dictionary at class level - extended to 14 days
        self.career_task = {
            "Full-Stack Developer": {
                1: {"Front-End Focus": "Work on a single HTML/CSS component (e.g., a navbar, a card). Make it pixel-perfect and responsive."},
                2: {"Back-End Focus": "Build a simple REST API endpoint in Flask (e.g., /api/tasks that returns a list of tasks)."},
                3: {"Integration": "Use JavaScript in your front-end to fetch data from your Flask API and display it dynamically on your HTML page."},
                4: {"Database Day": "Write a SQL query or use an ORM to add, read, update, or delete a record from your database."},
                5: {"Debugging & Polish": "Spend time fixing a known bug, improving code structure, or writing a simple test."},
                6: {"Learning & Exploration": "Watch a tutorial or read documentation about a concept you struggled with during the week (e.g., authentication, a CSS framework)."},
                7: {"Project & Deployment": "Work on a larger feature for your blog. Research one aspect of deployment (e.g., setting up a server, using Docker)."},
                8: {"Advanced Front-End": "Implement a complex UI component with state management (e.g., a shopping cart, a form wizard)."},
                9: {"Authentication & Security": "Add user authentication to your application using JWT or session-based authentication."},
                10: {"API Testing": "Write unit tests for your API endpoints using a testing framework like pytest or Jest."},
                11: {"Performance Optimization": "Profile your application and optimize bottlenecks (e.g., slow queries, large assets)."},
                12: {"Version Control": "Practice advanced Git operations like rebasing, cherry-picking, or resolving merge conflicts."},
                13: {"Code Review": "Review a peer's code or contribute to an open-source project."},
                14: {"Documentation": "Write comprehensive documentation for your project, including API docs and user guides."}
            },
            "Machine Learning Engineer": {
                1: {"Data Wrangling": "Clean, explore, and preprocess a dataset. Practice using pandas and visualization libraries."},
                2: {"Model Building": "Implement a machine learning model from scratch (using scikit-learn or TensorFlow/PyTorch) on a clean dataset."},
                3: {"Theory & Math": "Spend 30-60 minutes studying the mathematical fundamentals behind a specific algorithm (e.g., how gradient descent works, what loss functions are)."},
                4: {"Evaluation & Metrics": "Evaluate your model from Day 2. Calculate different metrics (accuracy, precision, recall, F1-score) and analyze where it failed."},
                5: {"Kaggle/Competition": "Actively participate in a Kaggle competition. This could be reading discussions, experimenting with new features, or trying a different model architecture."},
                6: {"Deep Learning": "Build and train a simple neural network, even if it's for a toy problem like MNIST digit classification."},
                7: {"Pipeline & MLOps": "Work on automating part of your workflow. Write a script to automatically preprocess data or look into tools like MLflow for experiment tracking."},
                8: {"Feature Engineering": "Practice advanced feature engineering techniques on a dataset."},
                9: {"Model Deployment": "Deploy a model as a REST API using Flask or FastAPI."},
                10: {"Hyperparameter Tuning": "Implement grid search, random search, or Bayesian optimization for hyperparameter tuning."},
                11: {"Ensemble Methods": "Implement ensemble methods like bagging, boosting, or stacking."},
                12: {"Time Series Analysis": "Work with time series data and implement forecasting models."},
                13: {"NLP Fundamentals": "Build a simple NLP application like sentiment analysis or text classification."},
                14: {"Model Interpretability": "Implement techniques like SHAP or LIME to explain model predictions."}
            },
            "Site Reliability Engineer": {
                1: {"Infrastructure as Code": "Write or modify a Terraform/CloudFormation script to define a piece of infrastructure (e.g., an S3 bucket, a VM)."},
                2: {"CI/CD Pipeline": "Work on a Jenkinsfile, GitHub Action, or GitLab CI configuration. Automate one step, like running tests or building a Docker image."},
                3: {"Containers & Orchestration": "Write a Dockerfile for a simple application or practice a kubectl command to manage Kubernetes pods."},
                4: {"Monitoring & Logging": "Set up a dashboard in Prometheus/Grafana or write a query in Splunk/ELK to analyze application logs."},
                5: {"Scripting & Automation": "Write a Bash or Python script to automate a repetitive system administration task (e.g., log rotation, health checks)."},
                6: {"Networking & Security": "Study a networking concept (e.g., TCP/IP, DNS, load balancers) or a security best practice (e.g., least privilege)."},
                7: {"Chaos Engineering & Post-Mortem": "Intentionally break something in a test environment and practice documenting the incident and recovery steps."},
                8: {"Service Mesh": "Implement a service mesh like Istio or Linkerd for a microservices application."},
                9: {"Backup & Disaster Recovery": "Design and implement a backup and disaster recovery strategy for a system."},
                10: {"Scaling Strategies": "Implement horizontal or vertical scaling for an application."},
                11: {"Security Hardening": "Apply security hardening techniques to a Linux server or container."},
                12: {"Cost Optimization": "Analyze and optimize cloud infrastructure costs."},
                13: {"Incident Response": "Practice incident response procedures in a simulated environment."},
                14: {"Performance Testing": "Conduct load testing and performance analysis on a system."}
            },
            "Mobile Development Specialist": {
                1: {"UI Construction": "Build a single screen in your app using SwiftUI, focusing on layout and basic user interaction."},
                2: {"Data & Logic": "Implement the data model and business logic for a feature (e.g., how to save a user's note, how to calculate a result)."},
                3: {"Navigation & Flow": "Work on app navigation, making sure screens connect properly and pass data between them."},
                4: {"API Integration": "Write network code to fetch data from a public API and display it in your app."},
                5: {"Platform Features": "Integrate a native iOS feature (e.g., Camera, Location Services, Notifications) into your app."},
                6: {"Performance & Debugging": "Profile your app for memory leaks or performance bottlenecks. Fix a bug or improve an animation."},
                7: {"App Store Prep": "Work on assets for the App Store (screenshots, description) or research the app review guidelines and provisioning profiles."},
                8: {"State Management": "Implement a state management solution like Redux, MobX, or Provider."},
                9: {"Offline Support": "Add offline functionality to your app using local storage or a database."},
                10: {"Animations": "Create complex animations and transitions in your app."},
                11: {"Testing": "Write unit tests and UI tests for your mobile application."},
                12: {"Accessibility": "Improve your app's accessibility features and test with accessibility tools."},
                13: {"Background Processing": "Implement background tasks or background fetch in your app."},
                14: {"App Analytics": "Integrate analytics and crash reporting into your app."}
            },
            "Cybersecurity Engineer": {
                1: {"Active Exploitation": "Work on an OSCP-like challenge box (from HTB, TryHackMe, or VulnHub). Focus on enumeration and initial access."},
                2: {"Privilege Escalation": "Practice privilege escalation techniques on the box from Day 1, either on Linux or Windows."},
                3: {"Defensive Security": "Analyze a sample of malicious code or network traffic (e.g., using Wireshark) to identify Indicators of Compromise (IOCs)."},
                4: {"Tool Proficiency": "Master a specific tool (e.g., nmap, Burp Suite, Metasploit). Learn one new switch or feature in depth."},
                5: {"Scripting for Security": "Write a small Python script to automate a penetration testing task (e.g., a custom fuzzer, a password cracker)."},
                6: {"Theory & Protocols": "Study the inner workings of a network protocol (e.g., TCP handshake, DNS, HTTP/S) or a common vulnerability class (e.g., SQLi, XSS)."},
                7: {"Documentation": "Write a detailed penetration test report for a machine you compromised during the week."},
                8: {"Web Application Security": "Practice identifying and exploiting web vulnerabilities in a deliberately vulnerable application."},
                9: {"Mobile Security": "Analyze a mobile app for security vulnerabilities."},
                10: {"Cryptography": "Implement or analyze cryptographic algorithms and protocols."},
                11: {"Malware Analysis": "Analyze a piece of malware in a sandboxed environment."},
                12: {"Threat Hunting": "Practice threat hunting techniques in a simulated environment."},
                13: {"Security Architecture": "Design a secure architecture for a system or application."},
                14: {"Compliance & Auditing": "Review a system against security standards like PCI DSS, ISO 27001, or NIST."}
            },
            "Data Engineer": {
                1: {"Data Ingestion": "Write a script to extract data from a source (e.g., a public API, a CSV file, a database) and land it in a staging area."},
                2: {"Data Transformation": "Write a SQL query or a PySpark script to clean, filter, and aggregate the data you ingested."},
                3: {"Data Orchestration": "Define or modify a task in an orchestration tool like Apache Airflow. Set up dependencies between tasks."},
                4: {"Data Warehousing": "Design a star or snowflake schema for a business problem. Practice writing efficient analytical queries against it."},
                5: {"Cloud & Distributed Systems": "Complete a tutorial or work with a specific cloud data service (e.g., AWS Glue, Google BigQuery, Azure Data Factory)."},
                6: {"Performance Tuning": "Analyze a slow-running query or job and try to optimize it (e.g., by adding an index, partitioning data, changing the execution plan)."},
                7: {"Monitoring & Quality": "Implement a data quality check (e.g., ensuring a column has no nulls, that counts are within expected ranges)."},
                8: {"Streaming Data": "Set up a streaming data pipeline using Kafka, Kinesis, or a similar technology."},
                9: {"Data Governance": "Implement data lineage tracking or metadata management."},
                10: {"Data Visualization": "Create dashboards or visualizations to represent data insights."},
                11: {"Data Lakes": "Design and implement a data lake architecture."},
                12: {"Real-time Analytics": "Implement real-time analytics on streaming data."},
                13: {"Data Privacy": "Implement data anonymization or pseudonymization techniques."},
                14: {"Data Modeling": "Design and implement a complex data model for a business domain."}
            }
        }
        
        # Generic tasks for careers not in template - extended to 14 days
        self.generic_tasks = {
            1: {"Foundation": "Review and understand the fundamental concepts and terminology of your field."},
            2: {"Practical Application": "Apply what you learned yesterday to a small, hands-on project or exercise."},
            3: {"Tool Exploration": "Research and try out a popular tool or software used in your career field."},
            4: {"Community Engagement": "Join an online community, forum, or social media group related to your career. Participate in discussions."},
            5: {"Goal Review": "Review your short-term and long-term goals. Break them down into smaller, actionable steps."},
            6: {"Learning Resource": "Find and review a high-quality learning resource (book, course, tutorial) for your career."},
            7: {"Networking": "Reach out to at least one professional in your field for advice or mentorship."},
            8: {"Skill Assessment": "Assess your current skill level in your field and identify areas for improvement."},
            9: {"Industry Trends": "Research current trends and future directions in your career field."},
            10: {"Portfolio Building": "Create or enhance a portfolio piece that showcases your skills."},
            11: {"Problem Solving": "Identify a common problem in your field and brainstorm potential solutions."},
            12: {"Case Study Analysis": "Find and analyze a case study relevant to your career field."},
            13: {"Professional Development": "Identify and plan for a certification or advanced training opportunity."},
            14: {"Reflection": "Reflect on what you've learned this week and how it applies to your career goals."}
        }
        
        # Load existing career choices when initializing
        self.load_career_choices()
        
        top = Frame(self, bg="#CFE8FF")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Goal Tracker", font=("Arial", 20, "bold"),bg="#CFE8FF").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", fg="white",height=1, width=10).pack(side="right", padx=12)

        goals_body = Frame(self, bd=1, relief="raised")
        goals_body.pack(fill="both", expand=True, padx=15, pady=5)
        goals_body.pack_propagate(False)

        # ----------- New UI -------------
        weltext = Frame(goals_body, bd=2, relief="raised", bg="#85C2FA")
        weltext.pack(fill="x")
        Label(weltext, text="Enter Your Own Career & Goals", font=("Arial", 20, "bold"), bg="#85C2FA").pack(padx=10)

        # Career input
        textentrybody = Frame(goals_body)
        textentrybody.pack(fill=X)
        Label(textentrybody, text="Career Name:", font=("Arial", 12, "bold")).pack(side=LEFT,padx=10, pady=15)
        self.career_entry = Entry(textentrybody, font=("Arial", 12), width=60)
        self.career_entry.pack(padx=5,side=LEFT)

        # Short-term input 
        short_tbody = Frame(goals_body)
        short_tbody.pack(fill=X)
        Label(short_tbody, text="Short-term Goal:", font=("Arial", 12, "bold")).pack(side=LEFT,padx=10, pady=15)
        self.short_term_entry = Text(short_tbody, height=3, width=80, font=("Arial", 12))
        self.short_term_entry.pack(padx=10, pady=5,side=LEFT)
        

        # Short-term time input (months) - Changed to Spinbox
        time_short_frame = Frame(goals_body)
        time_short_frame.pack(fill=X)
        Label(time_short_frame, text="Duration (Months):", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        
        # Create a frame for the spinbox and label
        month_spinbox_frame = Frame(time_short_frame)
        month_spinbox_frame.pack(side=LEFT, padx=5)
        
        # Initialize month variable for Spinbox
        self.month_var = StringVar(value="1")
        self.short_time_entry = Spinbox(
            month_spinbox_frame, 
            from_=1, 
            to=12, 
            width=8,
            font=("Arial", 12),
            textvariable=self.month_var,
            command=self.validate_month_spinbox
        )
        self.short_time_entry.pack(side=LEFT)
        
        Label(month_spinbox_frame, text="months", font=("Arial", 10)).pack(side=LEFT, padx=5)

        # Long-term input 
        long_tbody = Frame(goals_body)
        long_tbody.pack(fill=X)
        Label(long_tbody, text="Long-term Goal:", font=("Arial", 12, "bold")).pack(side=LEFT,padx=10, pady=15)
        self.long_term_entry = Text(long_tbody, height=3, width=80, font=("Arial", 12))
        self.long_term_entry.pack(side=LEFT,padx=10, pady=5)

        # Long-term time input (years) - Changed to Spinbox
        time_long_frame = Frame(goals_body)
        time_long_frame.pack(fill=X)
        Label(time_long_frame, text="Duration (Years):", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        
        # Create a frame for the spinbox and label
        year_spinbox_frame = Frame(time_long_frame)
        year_spinbox_frame.pack(side=LEFT, padx=5)
        
        # Initialize year variable for Spinbox
        self.year_var = StringVar(value="1")
        self.long_time_entry = Spinbox(
            year_spinbox_frame, 
            from_=1, 
            to=10, 
            width=8,
            font=("Arial", 12),
            textvariable=self.year_var,
            command=self.validate_year_spinbox
        )
        self.long_time_entry.pack(side=LEFT)
        
        Label(year_spinbox_frame, text="years", font=("Arial", 10)).pack(side=LEFT, padx=5)

        #Textbox - Modified to show career names
        textframe = Frame(goals_body)
        textframe.pack(fill=BOTH,padx=2,pady=10)
        Label(textframe,text="Your Careers:",font=("Arial", 12, "bold")).pack(side=TOP,padx=10)
        self.textbox =  Text(textframe,width=100, height=9, font=("Arial", 11))
        self.textbox.pack(pady=2)
        self.textbox.config(state=DISABLED)

        # Submit button
        submit = Button(goals_body, text="Submit", bg="blue", fg="white", width=30, height=2, command=self.submit_career)
        submit.pack(side=BOTTOM, pady=10)
        
        # Update the textbox with existing careers
        self.update_career_display()
    
    def on_show(self):
        """Called when the page is shown"""
        self.load_career_choices()
        self.update_career_display()
    
    def validate_month_spinbox(self):
        """Validation for month spinbox - always valid due to spinbox constraints"""
        # Spinbox already ensures value is between 1-12, so no need for validation
        return True
    
    def validate_year_spinbox(self):
        """Validation for year spinbox - always valid due to spinbox constraints"""
        # Spinbox already ensures value is between 1-10, so no need for validation
        return True
    
    def update_career_display(self):
        """Update the textbox to display only career names"""
        self.textbox.config(state=NORMAL)
        self.textbox.delete(1.0, END)
        
        if self.career_choices:
            self.textbox.insert(END, "Career Goals:\n\n")
            for i, career in enumerate(self.career_choices, 1):
                self.textbox.insert(END, f"{i}. {career}\n")
        else:
            self.textbox.insert(END, "No careers added yet.\n\nAdd your first career using the form above.")
        
        self.textbox.config(state=DISABLED)

    def submit_career(self):
        career = self.career_entry.get().strip()
        short_term = self.short_term_entry.get("1.0", END).strip()
        long_term = self.long_term_entry.get("1.0", END).strip()
        
        # Get values from spinboxes using the StringVar
        months = self.month_var.get()
        years = self.year_var.get()

        if not career or not short_term or not long_term:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        if career in self.career_choices:
            messagebox.showwarning("Duplicate", "You already created this career before.")
            return

        if messagebox.askokcancel("Confirm", f"Add career '{career}'?\n\nDuration: {months} month(s), {years} year(s)"):
            # save career with simplified format
            self.save_career_choice(career)

            # save user-defined goals with new format
            with open("tasks.txt", "a") as f:
                f.write(f"SHORTTERM:{career}|{short_term}|{months}\n")
                f.write(f"LONGTERM:{career}|{long_term}|{years}\n")

            # Find closest matching career template
            closest_career = self.find_closest_career(career)
            
            # Generate 14-day tasks using the closest career template or generic tasks
            if closest_career:
                self.generate_career_tasks(closest_career, career)
                messagebox.showinfo("Success", f"Career '{career}' added!\n\nYour 14 daily tasks are created based on {closest_career} template!")
            else:
                # Generate generic tasks for careers not in template
                self.generate_generic_tasks(career)
                messagebox.showinfo("Success", f"Career '{career}' added!\n\nYour 14 daily tasks are created with a generic template!")

            # Update the career display after adding
            self.update_career_display()

        # Clear form fields
        self.career_entry.delete(0, END)
        self.short_term_entry.delete("1.0", END)
        self.long_term_entry.delete("1.0", END)
        # Reset spinboxes using StringVar
        self.month_var.set("1")
        self.year_var.set("1")
    
    def find_closest_career(self, career):
        """Find the closest matching career template based on keywords"""
        career_lower = career.lower()
        
        # Define keyword mappings for each career
        career_keywords = {
            "Full-Stack Developer": ["full-stack", "full stack", "web", "developer", "frontend", "backend"],
            "Machine Learning Engineer": ["machine learning", "ml", "ai", "artificial intelligence", "data science"],
            "Site Reliability Engineer": ["sre", "site reliability", "devops", "infrastructure", "operations"],
            "Mobile Development Specialist": ["mobile", "ios", "android", "app", "smartphone"],
            "Cybersecurity Engineer": ["cybersecurity", "security", "penetration", "hacking", "network security"],
            "Data Engineer": ["data", "etl", "pipeline", "warehouse", "big data"]
        }
        
        # Check for keyword matches
        for template_career, keywords in career_keywords.items():
            for keyword in keywords:
                if keyword in career_lower:
                    return template_career
        
        # No direct match found, return None
        return None
    
    def generate_generic_tasks(self, career):
        """Generate generic weekly tasks for careers not in template."""
        today = date.today()
        
        with open("tasks.txt", "a") as f:
            for day_num in range(1, 15):  # Extended to 14 days
                if day_num in self.generic_tasks:
                    task_info = self.generic_tasks[day_num]
                    title = list(task_info.keys())[0]
                    description = list(task_info.values())[0]
                    
                    task_date = today + timedelta(days=day_num - 1)
                    
                    # Simplified format: TASK|career_detail|date|status
                    task_line = (
                        f"TASK|{career} - {title}: {description}|{task_date.strftime('%Y-%m-%d')}|pending\n"
                    )
                    f.write(task_line)
    
    def load_career_choices(self):
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
                    lines = content.strip().split('\n')
                    self.career_choices = []
                    for line in lines:
                        if line.startswith("CAREER|"):
                            career = line[7:].strip()
                            if career and career not in self.career_choices:
                                self.career_choices.append(career)
        except FileNotFoundError:
            self.career_choices = []
    
    def save_career_choice(self, career):
        try:
            with open("tasks.txt", "a") as f:
                f.write(f"CAREER|{career}\n")
                if career not in self.career_choices:
                    self.career_choices.append(career)
        except FileNotFoundError:
            with open("tasks.txt", "w") as f:
                f.write(f"CAREER|{career}\n")
                self.career_choices.append(career)
    
    def generate_career_tasks(self, template_career, user_career):
        """Generate weekly tasks for selected career and save them to tasks.txt."""
        today = date.today()
        
        with open("tasks.txt", "a") as f:
            for day_num in range(1, 15):  # Extended to 14 days
                if day_num in self.career_task[template_career]:
                    task_info = self.career_task[template_career][day_num]
                    title = list(task_info.keys())[0]
                    description = list(task_info.values())[0]
                    
                    task_date = today + timedelta(days=day_num - 1)
                    
                    # Simplified format: TASK|career_detail|date|status
                    task_line = (
                        f"TASK|{user_career} - {title}: {description}|{task_date.strftime('%Y-%m-%d')}|pending\n"
                    )
                    f.write(task_line)