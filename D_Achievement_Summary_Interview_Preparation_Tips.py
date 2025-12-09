# D_Achievement_Summary_Interview_Preparation_Tips.py
from tkinter import *
from tkinter import messagebox

class BaseAchievementPage(Frame):

    DATA_FILE = "achievement_data.txt"
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages

        top = Frame(self, bg="#3B68BD")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Achievement Summary & Interview Tips", font=("Arial", 18, "bold"),bg="#3B68BD").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red",fg="white" ,height=1, width=10).pack(side="right", padx=12)

        achievement_frame = Frame(self, bd=1, relief="raised")
        achievement_frame.pack(fill="both", expand=True, padx=12, pady=8)
        achievement_frame.pack_propagate(False)
        Label(achievement_frame, text="Achievement Summary", font=("Arial", 16, "bold")).pack(pady=10)

        self.summary_box = Text(achievement_frame, width=70, height=20, font=("Arial", 12))
        self.summary_box.pack(pady=5)

        button_frame = Frame(achievement_frame)
        button_frame.pack(pady=10)
        Button(button_frame, text="Generate Report", width=20,
                bg="#4a71f3", fg="white",command=self.show_report).pack(side="left", padx=10) 
        Button(button_frame, text="Refresh Summary", width=20,
                bg="#4a71f3", fg="white").pack(side="left", padx=10) #command=self.refresh_summary
        
        # go to QAPAge
        Button(
        achievement_frame,text="Go to Interview Q&A Manager",command=lambda: self.pages.show_frame("QAPage"),bg="#0696e9",fg="white",height=2,
        width=30).pack(side="bottom",pady=10)

    def show_report(self):
        """Generate a report based on the simplified tasks.txt format."""
        try:
            careers = []
            short_goals = []
            long_goals = []
            tasks = []
            completed_tasks = 0
            
            with open("tasks.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("CAREER|"):
                        careers.append(line[7:].strip())
                    elif line.startswith("SHORT|"):
                        short_goals.append(line[6:].strip())
                    elif line.startswith("LONG|"):
                        long_goals.append(line[5:].strip())
                    elif line.startswith("TASK|"):
                        parts = line.split('|')
                        if len(parts) >= 4:
                            tasks.append(parts[1].strip())
                            if parts[3].strip() == "completed":
                                completed_tasks += 1
            
            # Format the report
            report_text = "CAREER & SKILLS DEVELOPMENT REPORT\n"
            report_text += "=" * 50 + "\n\n"
            
            report_text += "CAREERS TRACKED:\n"
            for career in careers:
                report_text += f"• {career}\n"
            
            report_text += "\nSHORT-TERM GOALS:\n"
            for goal in short_goals:
                report_text += f"• {goal}\n"
                
            report_text += "\nLONG-TERM GOALS:\n"
            for goal in long_goals:
                report_text += f"• {goal}\n"
                
            report_text += f"\nTASKS COMPLETED: {completed_tasks} out of {len(tasks)}\n"
            
            # Display the report
            self.summary_box.delete(1.0, END)
            self.summary_box.insert(END, report_text)
            
        except FileNotFoundError:
            self.summary_box.delete(1.0, END)
            self.summary_box.insert(END, "No data found. Please add careers and goals first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")