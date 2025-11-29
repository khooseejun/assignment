from tkinter import *
from tkinter import messagebox

class BaseGoalPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages 
        top = Frame(self, bg="#CFE8FF")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Goal Tracker", font=("Arial", 20, "bold"),bg="#CFE8FF").pack(side="left", padx=12)
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
            if messagebox.askokcancel(title="Choose Career",message=f"Are you sure you want choose {career} ?"):
                if career not in career_list:
                    messagebox.showwarning(title="Choose a career",message="Choose a career, not choose a bug! :(")
                else:
                    messagebox.showinfo(title="Career Submit", message="Task submit")
            else:
                pass
            
        weltext = Frame(goals_body,bd=2, relief="raised")
        weltext.pack(fill="x")

        Label(weltext, text="Select Your Career\nLet Start You Target", font=("Arial", 20, "bold")).pack(padx=10)
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

        # next_btn = Button(goals_body, text="Next", command=show_career_details)
        # next_btn.pack()

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