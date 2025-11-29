from tkinter import *
from tkinter import messagebox

class BaseAchievementPage(Frame):

    DATA_FILE = "achievement_data.txt"
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages

        #     # 如果文件不存在就创建初始内容
        # if not os.path.exists(self.DATA_FILE):
        #     self.create_default_file()

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
        
        # # 初始载入
        # self.refresh_summary()

        # go to QAPAge
        Button(
        achievement_frame,text="Go to Interview Q&A Manager",command=lambda: self.pages.show_frame("QAPage"),bg="#0696e9",fg="white",height=2,
        width=30).pack(side="bottom",pady=10)

    # # ==============================
    # #      FILE HANDLING SECTION
    # # ==============================
    # def create_default_file(self):
    #     with open(self.DATA_FILE, "w") as f:
    #         f.write("goals_completed: 0\n")
    #         f.write("skills_acquired: \n")
    #         f.write("tasks_completed: 0\n")
    def show_report(self):
        report = {
            "goals_completed": 0,
            "skills_acquired": ["CSS", "HTML", "PYTHON"], 
            "tasks_completed": 0
        }
        
        # 将字典格式化为字符串
        report_text = f"Summary report:\n"
        report_text += f"• Goals completed: {report['goals_completed']}\n"
        report_text += f"• Skills acquired: {', '.join(report['skills_acquired'])}\n"
        report_text += f"• Tasks completed: {report['tasks_completed']}\n"
        
        # 清除文本框内容并插入新内容
        self.summary_box.delete(1.0, END)  # 清除现有内容
        self.summary_box.insert(END, report_text)  # 插入新内容

