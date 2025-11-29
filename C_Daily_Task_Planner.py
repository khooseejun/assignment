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
        self.career_filter_menu = OptionMenu(career_frame, self.career_filter_var, "All Careers", command=lambda _: self.apply_filters(self.current_date_filter, self.career_filter_var.get()))
        self.career_filter_menu.pack(pady=5)
        
        # Task statistics
        stats_frame = Frame(right_frame)
        stats_frame.pack(pady=10)
        
        self.stats_label = Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        # Task list frame with scrollbar
        list_frame = Frame(right_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.task_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode="single")
        self.task_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Task control buttons
        control_frame = Frame(right_frame)
        control_frame.pack(pady=10)
        
        Button(control_frame, text="Mark Complete", command=self.mark_complete, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        Button(control_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white").pack(side="left", padx=5)
        
        self.load_tasks()
    
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
                    # Use a set comprehension for cleaner, duplicate-free loading
                    self.career_choices = sorted(list({line[7:].strip() for line in lines if line.startswith("CAREER:")}))
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
        
        # Determine date range for filtering
        date_filtered = []
        if date_filter == "all":
            date_filtered = self.tasks
        elif date_filter == "today":
            date_filtered = [t for t in self.tasks if datetime.strptime(t["date"], "%Y-%m-%d").date() == today]
        elif date_filter == "tomorrow":
            date_filtered = [t for t in self.tasks if datetime.strptime(t["date"], "%Y-%m-%d").date() == tomorrow]
        elif date_filter == "week":
            date_filtered = [t for t in self.tasks if today <= datetime.strptime(t["date"], "%Y-%m-%d").date() <= week_end]

        # Apply career filter on top of the date filter
        if career_filter == "All Careers":
            self.filtered_tasks = date_filtered
        else:
            self.filtered_tasks = [t for t in date_filtered if t.get("career") == career_filter]
        
        self.update_task_list()
        self.update_statistics()
    
    def update_statistics(self):
        """Update task statistics display."""
        total_tasks = len(self.filtered_tasks)
        completed_tasks = sum(1 for task in self.filtered_tasks if task.get("completed"))
        career_tasks = sum(1 for task in self.filtered_tasks if task.get("is_career_task"))
        
        stats_text = f"Total: {total_tasks} | Completed: {completed_tasks} | Career Tasks: {career_tasks}"
        self.stats_label.config(text=stats_text)
    
    def load_tasks(self):
        """Load tasks from the text file."""
        try:
            with open("tasks.txt", "r") as f:
                self.tasks = []
                for line in f:
                    line = line.strip()
                    if not line.startswith("TASK|"):
                        continue
                    
                    parts = line.split('|')
                    # Ensure the line has the correct number of parts
                    if len(parts) < 8:
                        continue
                        
                    self.tasks.append({
                        "description": parts[1],
                        "date": parts[2],
                        "completed": parts[3].lower() == "true",
                        "career": parts[4] if parts[4] != "None" else None,
                        "day_of_week": int(parts[5]) if parts[5] != "None" else None,
                        "is_career_task": parts[6].lower() == "true",
                        "created_date": parts[7]
                    })
        except FileNotFoundError:
            self.tasks = []
    
    def save_tasks(self):
        """Save all tasks and career choices to the text file."""
        career_lines = []
        try:
            with open("tasks.txt", "r") as f:
                for line in f:
                    if line.startswith("CAREER:"):
                        career_lines.append(line.strip())
        except FileNotFoundError:
            career_lines = []
        
        with open("tasks.txt", "w") as f:
            for line in career_lines:
                f.write(line + "\n")
            
            for task in self.tasks:
                completed_str = "True" if task["completed"] else "False"
                career_task_str = "True" if task.get("is_career_task") else "False"
                # New format: TASK|description|date|completed|career|day_of_week|is_career_task|created_date
                f.write(f"TASK|{task['description']}|{task['date']}|{completed_str}|{task['career']}|{task['day_of_week']}|{career_task_str}|{task['created_date']}\n")
    
    def update_task_list(self):
        """Refresh the task listbox with filtered and sorted tasks."""
        self.task_listbox.delete(0, END)
        
        # Sort tasks: career tasks first, then by date
        sorted_tasks = sorted(
            self.filtered_tasks, 
            key=lambda t: (not t.get("is_career_task", False), t["date"])
        )
        
        for task in sorted_tasks:
            status = "✓" if task["completed"] else "○"
            career_tag = f"[{task.get('career')}] " if task.get("is_career_task") else ""
            display_text = f"{status} [{task['date']}] {career_tag}{task['description']}"
            self.task_listbox.insert(END, display_text)
    
    def _get_selected_task_from_listbox(self):
        """Helper to get the full task dictionary from the current listbox selection."""
        selection_indices = self.task_listbox.curselection()
        if not selection_indices:
            return None
            
        # Get the displayed text of the selected item
        selected_index = selection_indices[0]
        selected_text = self.task_listbox.get(selected_index)
        
        # Parse the text to find the task's date and description
        # Example text: "✓ [2023-10-27] [Full-Stack Developer] Build a simple REST API"
        try:
            parts = selected_text.split('] ', 2)
            task_date_str = parts[0][2:] # Remove "✓ [" or "○ ["
            task_description = parts[2]
            
            # Find the task in our main list using the parsed date and description
            for task in self.tasks:
                if task["date"] == task_date_str and task["description"] == task_description:
                    return task
        except IndexError:
            # This can happen if the display format is unexpected
            messagebox.showerror("Error", "Could not parse the selected task. Please check the format.")
            return None
            
        return None

    def mark_complete(self):
        """Toggle the 'completed' status of the selected task."""
        task = self._get_selected_task_from_listbox()
        if not task:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")
            return
            
        task["completed"] = not task["completed"]
        self.save_tasks()
        self.apply_filters(self.current_date_filter, self.current_career_filter)
    
    def delete_task(self):
        """Delete the selected task after confirmation."""
        task = self._get_selected_task_from_listbox()
        if not task:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this task?\n\n'{task['description']}'"):
            # Remove the task from the main list
            self.tasks.remove(task)
            self.save_tasks()
            self.apply_filters(self.current_date_filter, self.current_career_filter)
