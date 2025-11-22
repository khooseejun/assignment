from tkinter import *

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
        Button(buttons_frame, text="Achievement Summary & Interview Tips", command=lambda: self.pages.show_frame("AchievementPage"), **btn_opts).pack(pady=15)
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

        def show_career_details():
            career = selected_career.get()  # 取得 OptionMenu 的当前选择
            info = career_details[career]

            # 让 GUI 的 Label 显示内容
            output_label.config(
                text=f"{career}\n\n"
                    f"Short-term:\n{info['short_term']}\n\n"
                    f"Long-term:\n{info['long_term']}"
            )
            
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
        selected_career.set(career_list[0])
        
        OptionMenu(goals_body, selected_career, *career_list).pack(pady=10)

        next_btn = Button(goals_body, text="Next", command=show_career_details)
        next_btn.pack()

        output_label = Label(goals_body, text="", justify=LEFT,font=("Arial", 12, "bold"),anchor="w")
        output_label.pack(padx=10, pady=20, fill="both")

        submit = Button(goals_body, text="Submit", bg="blue",  width=30, height=2)
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
        top = Frame(self,bg="#FFFDFA")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Daily Task Planner", font=("Arial", 20, "bold"),bg="#FFFDFA").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        planner_frame = Frame(self, bd=1, relief="raised")
        planner_frame.pack(fill="both", expand=True, padx=12, pady=8)
        taskFrame = Frame(planner_frame,bg="#FFFDFA")
        taskFrame.pack(side=LEFT)

        # Simulate get data to allTask
        allTask = ["Programming","Full Stack", "Artifical Intelligence", "IOS Mobile Development", "Cybersecurity", "Database"]
        checktaskvalue = [BooleanVar(value=False) for _ in allTask]

        for allTask2, checktaskvalue2 in zip(allTask, checktaskvalue):
            checktask = Checkbutton(taskFrame,text=allTask2,variable=checktaskvalue2,onvalue=1,offvalue=0).pack(anchor='w')

class AchievementPage(BasePage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)
        top = Frame(self)
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Achievement Summary & Interview Tips", font=("Arial", 18, "bold")).pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        achievement_frame = Frame(self, bd=1, relief="raised")
        achievement_frame.pack(fill="both", expand=True, padx=12, pady=8)
        Label(achievement_frame, text="achievement_frame function write here", font=("Arial", 15, "bold")).pack(anchor="center", expand=True)



if __name__ == "__main__":
    MainMenu().mainloop()