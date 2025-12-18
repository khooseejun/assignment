from tkinter import *
from A_Goal_Tracker import *
from B_Skills_Log import *
from C_Daily_Task_Planner import *
from D_Achievement_Summary_Interview_Preparation_Tips import *

class BasePage(Frame):
    """All pages inherit from this base for convenience"""
    def __init__(self, parent, pages):
        super().__init__(parent)
        # store reference to the "pages" controller (previously named controller)
        self.pages = pages

class MainMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title("Main menu")
        self.geometry("900x600")
        # self.resizable(False, False)
        container = Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, GoalPage, PlannerPage, SkillsLogPage,AchievementPage, QAPage):
            page_name = F.__name__
            # pass self as "pages" (previously passed as controller)
            frame = F(parent=container, pages=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("HomePage")

            # Initialize tasks.txt file if it doesn't exist
        self.initialize_tasks_file()

    def initialize_tasks_file(self):
        """Create tasks.txt if it doesn't exist"""
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
        except FileNotFoundError:
            # Create the file if it doesn't exist
            with open("tasks.txt", "w") as f:
                f.write("")

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
        header = Frame(self, height=100, bg= "#313D85")
        header.pack(side="top", fill="x")
        header.pack_propagate(False)
        Label(header, text="Quantum\nLeap", font=("Arial", 30, "bold italic"),fg="#004FFA",bg = "#313D85").pack(anchor="center",expand=True)
        
        body = Frame(self, bg="#4B6CB7")
        body.pack(fill="both")
        move_text = Frame(body,relief="flat")
        move_text.pack(fill="y")
        m_frame = Frame(move_text, relief="flat",bg="#4B6CB7")
        m_frame.pack(side="left", fill="y")
        self.m_canvas = Canvas(m_frame, width=900, height=50, bg="#3EA7EC",relief="flat")
        self.m_canvas.pack(pady=15)
        self.m_text = self.m_canvas.create_text(
            0, 25, text="Career & Skills Development Assistant Apps", font=("Arial", 14),anchor="w", tags="move_text")
        self.x = 0
        self.scroll_m_text()

        buttons_frame = Frame(body, bg="#4B6CB7", relief="flat")
        buttons_frame.pack(padx=8)
        btn_opts = {"font" :"Arial, 10","width": 40, "height": 2, "bd": 3, "relief": "raised","activebackground": "#1F3A73"}
        Button(buttons_frame, text="Goal Tracker", command=lambda: self.pages.show_frame("GoalPage"), **btn_opts).pack(pady=17)
        Button(buttons_frame, text="Skills Log", command=lambda: self.pages.show_frame("SkillsLogPage"), **btn_opts).pack(pady=17)
        Button(buttons_frame, text="Daily Task Planner", command=lambda: self.pages.show_frame("PlannerPage"), **btn_opts).pack(pady=17)
        Button(buttons_frame, text="Achievement Summary & Interview Tips", command=lambda: self.pages.show_frame("AchievementPage"), **btn_opts).pack(pady=17)
        Button(buttons_frame, text="Exit", command=self.pages.quit, **btn_opts,bg="#00c9fc").pack(pady=17)

    def scroll_m_text(self):
        width = 850
        dx = 1
        self.m_canvas.move("move_text", dx, 0)
        self.x += dx
        if self.x > width:
            self.x = 0
            self.m_canvas.delete("move_text")
            self.m_text = self.m_canvas.create_text(
                self.x, 25, text="Career & Skills Development Assistant Apps",
                font=("Arial", 13), anchor="w", tags="move_text" )
        self.m_canvas.after(50, self.scroll_m_text)


class GoalPage(BaseGoalPage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)


class PlannerPage(BasePlannerPage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)


class SkillsLogPage(BaseSkillsLogPage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)


class AchievementPage(BaseAchievementPage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)

        
class QAPage(BaseQAPage):
    def __init__(self, parent, pages):
        super().__init__(parent, pages)


if __name__ == "__main__":
    MainMenu().mainloop()