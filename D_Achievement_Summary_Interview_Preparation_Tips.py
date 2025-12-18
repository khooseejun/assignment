from tkinter import *
from tkinter import messagebox

# ===============================
# BaseAchievementPage: Handles achievement summary display, report generation, progress
# and navigation to Q&A manager
# ===============================
class BaseAchievementPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages # reference to main application for page switching

        # ----- Top Header Section -----
        top = Frame(self, bg="#3B68BD")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Achievement Summary & Interview Tips", font=("Arial", 18, "bold"), 
              bg="#3B68BD").pack(side="left", padx=12)
        # Back button returns to HomePage
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), 
               bg="red", fg="white", height=1, width=10).pack(side="right", padx=12)

        # ----- Main Achievement Summary Frame -----
        achievement_frame = Frame(self, bd=1, relief="raised", bg="#DDE6F3")
        achievement_frame.pack(fill="both", expand=True, padx=12, pady=8)
        achievement_frame.pack_propagate(False)
        Label(achievement_frame, text="Achievement Summary", font=("Arial", 16, "bold"), fg="#1277CA",bg="#DDE6F3").pack(pady=10)

        # Text box showing full achievement report
        self.summary_box = Text(achievement_frame, width=90, height=20, font=("Arial", 12),fg="#2C3E50")
        self.summary_box.pack(pady=5)

        # Button options under summary
        button_frame = Frame(achievement_frame, bg="#DDE6F3")
        button_frame.pack(pady=10)
        Button(button_frame, text="Generate Report", width=20,
               bg="#4a71f3",  command=self.show_report).pack(side="left", padx=10)
        self.refresh_btn = Button(
            button_frame,text="Refresh Summary",width=20,bg="#9AB3F8",
            state=DISABLED, command=self.refresh_summary)
        self.refresh_btn.pack(side="left", padx=10)

        # Redirect to Interview Q&A Manager
        Button(
            achievement_frame,text="Go to Interview Q&A Manager",command=lambda: self.pages.show_frame("QAPage"),bg="#00ff15", height=2, width=30
        ).pack(side="bottom", pady=10)

    # ------------------------------
    # LOAD MULTIPLE CAREERS + GOALS
    # Reads tasks.txt and organizes careers with short- and long-term goals
    # ------------------------------
    def load_career_and_goals(self):
        careers = {}

        try:
            with open("tasks.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    # # CAREER|Name → create career entry
                    if line.startswith("CAREER|"):
                        parts = line.split("|")
                        if len(parts) >= 2:
                            name = parts[1].strip()
                            if name not in careers:
                                careers[name] = {"short": None, "long": None}

                    # # SHORTTERM:Career|goal|time → store short-term goal
                    elif line.startswith("SHORTTERM:"):
                        parts = line.split("|")
                        if len(parts) >= 3:
                            career_name = parts[0].split(":")[1].strip()
                            goal = parts[1].strip()
                            time = parts[2].strip() + " month"

                            # auto-add career if missing
                            if career_name not in careers:
                                careers[career_name] = {"short": None, "long": None}
                            else: #原本是 careers[career_name]["short"] = (goal, time), 没有else
                                careers[career_name]["short"] = (goal, time)

                    # # LONGTERM:Career|goal|time → store long-term goal
                    elif line.startswith("LONGTERM:"):
                        parts = line.split("|")
                        if len(parts) >= 3:
                            career_name = parts[0].split(":")[1].strip()
                            goal = parts[1].strip()
                            time = parts[2].strip() + " year"

                            if career_name not in careers:
                                careers[career_name] = {"short": None, "long": None}
                            else: #原本是 careers[career_name]["long"] = (goal, time) , 没有else
                                careers[career_name]["long"] = (goal, time)

        except FileNotFoundError:
            return {} # No file → return empty

        return careers

    # ------------------------------
    # LOAD SKILLS
    # Reads skills_log.txt and extracts skill names
    # ------------------------------
    def load_skills(self):
        skills = []
        try:
            with open("skills_log.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skills stored as: [Skill] SkillName
                    if line.startswith("[Skill]"):
                        skill_name = line.replace("[Skill]", "").strip()
                        if skill_name:
                            skills.append(skill_name)
        except FileNotFoundError:
            return []
        return skills

    # ------------------------------
    # COUNT COMPLETED TASKS
    # Parses tasks.txt and counts entries ending with "completed"
    # ------------------------------
    def count_completed_tasks(self):
        count = 0
        try:
            with open("tasks.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line.startswith("TASK|"):
                        continue

                    parts = line.split("|")
                    if len(parts) < 3:
                        continue  # Skip invalid format

                    status = parts[-1].strip().lower()  # Last part always status

                    if status == "completed":
                        count += 1

        except FileNotFoundError:
            return 0

        return count

    # ------------------------------
    # FORMAT CAREER SECTION
    # Converts career+goal data to readable text
    # ------------------------------
    def format_career_output(self, careers):
        text = "Career Path Selected:\n"

        if not careers:
            return text + "• None\n\n"

        for career, goals in careers.items():
            text += f"• {career}\n"

            # Short-term goal
            text += " -Short-Term Goal:  "
            if goals["short"]:
                goal, t = goals["short"]
                text += f"{goal} ({t})\n"
            else:
                text += "None\n"

            # Long-term goal
            text += " -Long-Term Goal:   "
            if goals["long"]:
                goal, t = goals["long"]
                text += f"{goal} ({t})\n"
            else:
                text += "None\n"

            text += "\n"

        return text

    # ------------------------------
    # SHOW REPORT
    # Generates formatted achievement summary and prints to text box
    # ------------------------------
    def show_report(self):
        careers = self.load_career_and_goals()
        skills = self.load_skills()
        tasks_completed = self.count_completed_tasks()

        # ================================
        #  NO DATA CHECK
        # ================================
        if not careers and len(skills) == 0 and tasks_completed == 0:
            messagebox.showinfo("No Data", "You currently have no recorded career, skills, or tasks.\nPlease add some data before generating a report.")
            return

        if not skills:
            skills = ["No skills recorded yet"]

        # Header
        report_text = (
            "\t\t\t\t=========================\n"
            "\t\t\t\t  Achievement Summary Report\n"
            "\t\t\t\t=========================\n\n"
        )

        # Career section
        report_text += self.format_career_output(careers)

        report_text += "---------------------------------------\n\n"
        # Skills + Tasks
        report_text += f"Skills Acquired: {', '.join(skills)}\n"
        report_text += "\n-------------------------------------\n"
        report_text += f"\nTasks Completed: {tasks_completed}\n"

        report_text += "\n======================================================================"
        # ======================================
        # Progress Bar
        # ======================================

        # ---- 1. percentage score ----
        task_score = min(tasks_completed / 365, 1)
        skill_score = min(len(skills) / 12, 1)
        progress_percent = int((task_score + skill_score) / 2 * 100)

        # ---- 2. level ----
        if progress_percent >= 85:
            progress_level = "Excellent"
        elif progress_percent >= 60:
            progress_level = "Advanced"
        elif progress_percent >= 35:
            progress_level = "Intermediate"
        else:
            progress_level = "Beginner"

        # ---- 3. text progress bar ----
        bar_length = 50  # total bar size
        filled_length = int(bar_length * progress_percent / 100)

        bar = "█" * filled_length + "-" * (bar_length - filled_length)

        report_text += "\nProgress\n"
        report_text += f"[{bar}] {progress_percent}%\n"
        report_text += f"Level: {progress_level}\n"
        # Achievement evaluation
        report_text += "\nComments"
        if tasks_completed >= 84 and len(skills) >= 9:
            report_text += "\n⭐ Excellent performance! Keep it up! ⭐\n"
        else:
            report_text += "\n💪 Keep up the good work, you can do even better!! 💪\n"

        # # Display in text widget (read-only)
        self.summary_box.config(state=NORMAL)
        self.summary_box.delete("1.0", END)
        self.summary_box.insert(END, report_text)
        self.summary_box.config(state=DISABLED)

        self.refresh_btn.config(state=NORMAL)

    # ------------------------------
    # REFRESH SUMMARY (same as show_report)
    # ------------------------------
    def refresh_summary(self):
        self.show_report()  # Same logic, reuse


# ===============================
# BaseQAPage: Saves interview Q&A pairs and displays them
# ===============================
class BaseQAPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages

        # ----- Header -----
        top = Frame(self, bg="#f5f5f5")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Interview Q&A Manager", font=("Arial", 22, "bold"), bg="#f5f5f5",fg="#0077ff").pack(side="left", padx=12)
        # back button to AchievementPage
        Button(top, text="Back", command=lambda: self.pages.show_frame("AchievementPage"),
               bg="red", fg="white",height=1, width=10).pack(side="right", padx=12)

        # ----- Body section containing input fields -----
        body = Frame(self, bd=1, relief="raised")
        body.pack(fill="both", expand=True, padx=12, pady=8)
        body.pack_propagate(False)

        # --- Question Input ---
        # User provides a question here
        saveQA = Frame(body, bd=2)
        saveQA.pack(fill="x")
        Label(saveQA, text="Question:", font=("Arial", 15, "bold"),fg="blue").pack(pady=4,side=LEFT)
        self.q_entry = Entry(saveQA, width=130)
        self.q_entry.pack(pady=2,side=LEFT)

        # --- Answer Input Section ---
        saveAS = Frame(body,bd=2)
        saveAS.pack(fill="x")
        Label(saveAS, text="Answer:", font=("Arial", 15, "bold"),fg="blue").pack(side=LEFT,pady=4)
        self.a_entry = Entry(saveAS, width=130)
        self.a_entry.pack(pady=2,side=LEFT)

        # Save Q&A button
        # When clicked → writes Q&A pair into file and refreshes list
        Button(body, text="Save Q&A", bg="#4a71f3", fg="white",width=20,command=self.save_qa).pack(pady=10) 

        # Separator
        Frame(body, height=2, bg="black").pack(fill="x", pady=10)

        QandA_frame = Frame(body, bd=2)
        QandA_frame.pack(fill="both",pady=10,padx=10)
        # --- All Q&A Display Section ---
        Label(QandA_frame, text="All Q&A:", font=("Arial", 12, "bold")).pack(anchor="w", pady=4)
        
        # Text widget showing all stored questions and answers
        self.qa_text = Text(QandA_frame, width=100, height=20, font=("Arial", 12))
        self.qa_text.pack(pady=2)
        self.qa_text.config(state=DISABLED)  # 默认不可编辑

        # load existing data at start
        self.load_qa()

    # File where Q&A pairs are stored
    DATA_FILE = "Q&A_sets.txt"
    # -------------------------
    # Save Q&A Function
    # Stores the question and answer as a single line formatted with '|'
    # -------------------------
    def save_qa(self):
        q = self.q_entry.get().strip()
        a = self.a_entry.get().strip()

        # Validate user input
        if not q or not a:
            return  messagebox.showinfo(title="Submit fail!!", message="You haven't filled in all the blanks!!")
        # Save into file
        with open(self.DATA_FILE, "a", encoding="utf-8") as f:
            f.write(q + "|" + a + "\n")

        # # Clear input fields after saving
        self.q_entry.delete(0, END)
        self.a_entry.delete(0, END)

        self.load_qa()  # refresh display

    # -------------------------
    # Load & Print All Q&A
    # Reads each Q&A pair and prints them in readable format
    # -------------------------
    def load_qa(self):
        # Allow editing temporarily to update content
        self.qa_text.config(state=NORMAL)
        self.qa_text.delete("1.0", END)

        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    # Skip corrupt lines
                    if "|" not in line:
                        continue
                    # Separate question and answer
                    q, a = line.strip().split("|", 1)
                    # Display nicely formatted Q&A
                    self.qa_text.insert(END, f"Q: {q}\nA: {a}\n\n")
        except FileNotFoundError:
            # If file missing, no crash — simply show nothing
            print("Error, file got some problem!!")
            pass

        # Set widget back to read-only
        self.qa_text.config(state=DISABLED)