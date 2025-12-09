# C_Daily_Task_Planner.py
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta

class BasePlannerPage(Frame):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages
        
        self.tasks = []
        self.filtered_tasks = []
        self.career_choices = []
        self.current_date_filter = "all"
        self.current_career_filter = "All Careers"
        
        top = Frame(self,bg="#FFFDFA")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Daily Task Planner", font=("Arial", 20, "bold"),bg="#FFFDFA").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        main_container = Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Task list frame - now takes full width
        task_frame = Frame(main_container, bd=1, relief="raised")
        task_frame.pack(side="right", fill="both", expand=True)
        
        Label(task_frame, text="Task List", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Filter buttons
        filter_frame = Frame(task_frame)
        filter_frame.pack(pady=10)
        
        Label(filter_frame, text="Filter by Date:").pack()
        
        date_button_frame = Frame(filter_frame)
        date_button_frame.pack(pady=5)
        
        Button(date_button_frame, text="All", command=lambda: self.apply_filters("all", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="Today", command=lambda: self.apply_filters("today", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="Tomorrow", command=lambda: self.apply_filters("tomorrow", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="This Week", command=lambda: self.apply_filters("week", self.current_career_filter), width=10).pack(side="left", padx=2)
        
        # Career filter
        career_frame = Frame(task_frame)
        career_frame.pack(pady=10)
        
        Label(career_frame, text="Filter by Career:").pack()
        
        self.career_filter_var = StringVar()
        self.career_filter_var.set("All Careers")
        self.career_filter_menu = OptionMenu(career_frame, self.career_filter_var, "All Careers", command=lambda _: self.apply_filters(self.current_date_filter, self.career_filter_var.get()))
        self.career_filter_menu.pack(pady=5)
        
        # Task statistics
        stats_frame = Frame(task_frame)
        stats_frame.pack(pady=10)
        
        self.stats_label = Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        # Task list frame with scrollbar
        list_frame = Frame(task_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.task_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode="single")
        self.task_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Task control buttons
        control_frame = Frame(task_frame)
        control_frame.pack(pady=10)
        
        Button(control_frame, text="Mark Complete", command=self.mark_complete, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        Button(control_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white").pack(side="left", padx=5)
        
        # Load tasks on initialization
        self.after(100, self.on_show)  # Delay to ensure UI is fully loaded
    
    def on_show(self):
        self.load_tasks()
        self.load_career_choices()
        self.update_career_filter()
        self.apply_filters("all", "All Careers")
        self.update_statistics()
    
    def load_career_choices(self):
        """Load career choices from text file."""
        try:
            with open("tasks.txt", "r") as f:
                content = f.read()
                if content:
                    lines = content.strip().split('\n')
                    self.career_choices = sorted(list({line[7:].strip() for line in lines if line.startswith("CAREER|")}))
        except FileNotFoundError:
            self.career_choices = []
    
    def update_career_filter(self):
        """Update the career filter dropdown menu."""
        menu = self.career_filter_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All Careers", command=lambda: self.apply_filters(self.current_date_filter, "All Careers"))
        for career in self.career_choices:
            menu.add_command(label=career, command=lambda c=career: self.apply_filters(self.current_date_filter, c))
    
    def apply_filters(self, date_filter, career_filter):
        """Apply date and career filters to the task list."""
        self.current_date_filter = date_filter
        self.current_career_filter = career_filter
        self.career_filter_var.set(career_filter)
        
        today, tomorrow = date.today(), date.today() + timedelta(days=1)
        week_end = today + timedelta(days=7)
        
        date_filtered = []
        if date_filter == "all":
            date_filtered = self.tasks
        elif date_filter == "today":
            date_filtered = [t for t in self.tasks if datetime.strptime(t["date"], "%Y-%m-%d").date() == today]
        elif date_filter == "tomorrow":
            date_filtered = [t for t in self.tasks if datetime.strptime(t["date"], "%Y-%m-%d").date() == tomorrow]
        elif date_filter == "week":
            date_filtered = [t for t in self.tasks if today <= datetime.strptime(t["date"], "%Y-%m-%d").date() <= week_end]

        if career_filter == "All Careers":
            self.filtered_tasks = date_filtered
        else:
            self.filtered_tasks = [t for t in date_filtered if career_filter in t["description"]]
        
        self.update_task_list()
        self.update_statistics()
    
    def update_statistics(self):
        """Update task statistics display."""
        total_tasks = len(self.filtered_tasks)
        completed_tasks = sum(1 for task in self.filtered_tasks if task.get("status") == "completed")
        
        stats_text = f"Total: {total_tasks} | Completed: {completed_tasks}"
        self.stats_label.config(text=stats_text)
    
    def load_tasks(self):
        """Load tasks from the text file with simplified format."""
        try:
            with open("tasks.txt", "r") as f:
                self.tasks = []
                for line in f:
                    line = line.strip()
                    if not line.startswith("TASK|"):
                        continue
                    
                    parts = line.split('|')
                    if len(parts) < 4:
                        continue
                        
                    # Simplified format: TASK|career_detail|date|status
                    self.tasks.append({
                        "description": parts[1],
                        "date": parts[2],
                        "status": parts[3]  # "pending" or "completed"
                    })
        except FileNotFoundError:
            self.tasks = []
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save all tasks and career choices to the text file with simplified format."""
        career_lines = []
        shortterm_lines = []
        longterm_lines = []
        
        try:
            with open("tasks.txt", "r") as f:
                for line in f:
                    if line.startswith("CAREER|"):
                        career_lines.append(line.strip())
                    elif line.startswith("SHORTTERM:"):
                        shortterm_lines.append(line.strip())
                    elif line.startswith("LONGTERM:"):
                        longterm_lines.append(line.strip())
        except FileNotFoundError:
            career_lines = []
            shortterm_lines = []
            longterm_lines = []
        
        with open("tasks.txt", "w") as f:
            # Write back career choices
            for line in career_lines:
                f.write(line + "\n")
            
            # Write back short-term goals
            for line in shortterm_lines:
                f.write(line + "\n")
                
            # Write back long-term goals
            for line in longterm_lines:
                f.write(line + "\n")
            
            # Write all tasks with simplified format
            for task in self.tasks:
                f.write(f"TASK|{task['description']}|{task['date']}|{task['status']}\n")
    
    def update_task_list(self):
        """Refresh the task listbox with filtered and sorted tasks."""
        self.task_listbox.delete(0, END)
        
        if not self.filtered_tasks:
            self.task_listbox.insert(END, "No tasks found")
            return
        
        sorted_tasks = sorted(self.filtered_tasks, key=lambda t: t["date"])
        
        for task in sorted_tasks:
            status = "✓" if task["status"] == "completed" else "○"
            display_text = f"{status} [{task['date']}] {task['description']}"
            self.task_listbox.insert(END, display_text)
    
    def _get_selected_task_from_listbox(self):
        """Helper to get the full task dictionary from the current listbox selection."""
        selection_indices = self.task_listbox.curselection()
        if not selection_indices:
            return None
            
        selected_index = selection_indices[0]
        selected_text = self.task_listbox.get(selected_index)
        
        # Skip if it's the "No tasks found" message
        if selected_text == "No tasks found":
            return None
        
        try:
            # Split the string into parts. Max 2 splits.
            # Example: "✓ [2023-10-27] Full-Stack Developer - Build a simple REST API"
            parts = selected_text.split('] ', 1)
            
            # Extract date from the first part, e.g., "✓ [2023-10-27"
            task_date_str = parts[0].split('[')[1].strip()
            task_description = parts[1].strip()

            # Find the task in our main list using the parsed date and description
            for task in self.tasks:
                if task["date"] == task_date_str and task["description"] == task_description:
                    return task
        except (IndexError, KeyError):
            # This can happen if the display format is unexpected
            print(f"DEBUG: Parsing failed for text: {selected_text}") # Debug print
            messagebox.showerror("Error", f"Could not parse the selected task.\nText: {selected_text}")
            return None
            
        return None

    def mark_complete(self):
        """Toggle the 'completed' status of the selected task."""
        task = self._get_selected_task_from_listbox()
        if not task:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")
            return
            
        task["status"] = "completed" if task["status"] == "pending" else "pending"
        self.save_tasks()
        self.apply_filters(self.current_date_filter, self.current_career_filter)
    
    def delete_task(self):
        """Delete the selected task after confirmation."""
        task = self._get_selected_task_from_listbox()
        if not task:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this task?\n\n'{task['description']}'"):
            self.tasks.remove(task)
            self.save_tasks()
            self.apply_filters(self.current_date_filter, self.current_career_filter)