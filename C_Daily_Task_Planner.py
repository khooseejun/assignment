from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta

class BasePlannerPage(Frame):
    """
    A class for creating a daily task planner page in a tkinter application.
    Allows users to view, filter, mark complete, and delete tasks.
    """
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages  # Reference to the page manager for navigation
        
        # Initialize data structures
        self.tasks = []  # List to store all tasks
        self.filtered_tasks = []  # List to store tasks after applying filters
        self.career_choices = []  # List to store career choices for filtering
        self.current_date_filter = "all"  # Current date filter state
        self.current_career_filter = "All Careers"  # Current career filter state
        
        # Create the top frame with title and back button
        top = Frame(self,bg="#FFFDFA")
        top.pack(fill="x", pady=8, padx=10)
        Label(top, text="Daily Task Planner", font=("Arial", 20, "bold"),bg="#FFFDFA").pack(side="left", padx=12)
        Button(top, text="Back", command=lambda: self.pages.show_frame("HomePage"), bg="red", height=1, width=10).pack(side="right", padx=12)

        # Main container for all UI elements
        main_container = Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Task list frame - now takes full width
        task_frame = Frame(main_container, bd=1, relief="raised")
        task_frame.pack(side="right", fill="both", expand=True)
        
        # Title for the task list
        Label(task_frame, text="Task List", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Filter buttons frame
        filter_frame = Frame(task_frame)
        filter_frame.pack(pady=10)
        
        Label(filter_frame, text="Filter by Date:").pack()
        
        # Date filter buttons
        date_button_frame = Frame(filter_frame)
        date_button_frame.pack(pady=5)
        
        Button(date_button_frame, text="All", command=lambda: self.apply_filters("all", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="Today", command=lambda: self.apply_filters("today", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="Tomorrow", command=lambda: self.apply_filters("tomorrow", self.current_career_filter), width=10).pack(side="left", padx=2)
        Button(date_button_frame, text="This Week", command=lambda: self.apply_filters("week", self.current_career_filter), width=10).pack(side="left", padx=2)
        
        # Career filter frame
        career_frame = Frame(task_frame)
        career_frame.pack(pady=10)
        
        Label(career_frame, text="Filter by Career:").pack()
        
        # Career filter dropdown menu
        self.career_filter_var = StringVar()
        self.career_filter_var.set("All Careers")
        self.career_filter_menu = OptionMenu(career_frame, self.career_filter_var, "All Careers", command=lambda _: self.apply_filters(self.current_date_filter, self.career_filter_var.get()))
        self.career_filter_menu.pack(pady=5)
        
        # Task statistics frame
        stats_frame = Frame(task_frame)
        stats_frame.pack(pady=10)
        
        self.stats_label = Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        # Task table frame with scrollbar
        table_frame = Frame(task_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create a Treeview with columns - now with separate columns for career, title, and description
        columns = ("status", "date", "career", "title", "description")
        self.task_tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define headings
        self.task_tree.heading("status", text="✓")
        self.task_tree.heading("date", text="Date")
        self.task_tree.heading("career", text="Career")
        self.task_tree.heading("title", text="Task Title")
        self.task_tree.heading("description", text="Description")
        
        # Configure column widths
        self.task_tree.column("status", width=30, minwidth=30, anchor="center", stretch=False)
        self.task_tree.column("date", width=80, minwidth=75, anchor="center", stretch=False)
        self.task_tree.column("career", width=120, minwidth=100, anchor="w", stretch=False)
        self.task_tree.column("title", width=150, minwidth=120, anchor="w", stretch=False)
        self.task_tree.column("description", width=400, minwidth=200, anchor="w", stretch=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.task_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure alternating row colors and styling
        self.task_tree.tag_configure("oddrow", background="#F5F5F5")
        self.task_tree.tag_configure("evenrow", background="white")
        self.task_tree.tag_configure("completed", foreground="green")
        self.task_tree.tag_configure("pending", foreground="black")
        
        # Configure style for better readability
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Task control buttons frame
        control_frame = Frame(task_frame)
        control_frame.pack(pady=10)
        
        # Buttons to mark tasks complete or delete them
        Button(control_frame, text="Mark Complete", command=self.mark_complete, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        Button(control_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white").pack(side="left", padx=5)
        
        # Load tasks on initialization
        self.after(100, self.on_show)  # Delay to ensure UI is fully loaded
    
    def on_show(self):
        """Called when the page is shown to refresh the task list and filters"""
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
        
        # Get date ranges for filtering
        today, tomorrow = date.today(), date.today() + timedelta(days=1)
        week_end = today + timedelta(days=7)
        
        # Apply date filter
        date_filtered = []
        if date_filter == "all":
            date_filtered = self.tasks
        elif date_filter == "today":
            date_filtered = [t for t in self.tasks if datetime.strptime(t["date"], "%Y-%m-%d").date() == today]
        elif date_filter == "tomorrow":
            date_filtered = [t for t in self.tasks if datetime.strptime(t["date"], "%Y-%m-%d").date() == tomorrow]
        elif date_filter == "week":
            date_filtered = [t for t in self.tasks if today <= datetime.strptime(t["date"], "%Y-%m-%d").date() <= week_end]

        # Apply career filter
        if career_filter == "All Careers":
            self.filtered_tasks = date_filtered
        else:
            self.filtered_tasks = [t for t in date_filtered if career_filter in t["career"]]
        
        # Update the task list display
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
                        
                    # Parse the task description to extract career, title, and description
                    description = parts[1]
                    career = ""
                    title = ""
                    task_desc = ""
                    
                    # Try to parse the description format: "career - title: description"
                    if " - " in description and ": " in description:
                        career_part, rest = description.split(" - ", 1)
                        career = career_part.strip()
                        
                        if ": " in rest:
                            title_part, desc_part = rest.split(": ", 1)
                            title = title_part.strip()
                            task_desc = desc_part.strip()
                        else:
                            title = rest.strip()
                            task_desc = ""
                    else:
                        # If parsing fails, use the entire description as task description
                        task_desc = description
                    
                    # Simplified format: TASK|career_detail|date|status
                    self.tasks.append({
                        "career": career,
                        "title": title,
                        "description": task_desc,
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
                # Reconstruct the original description format
                if task["title"]:
                    description = f"{task['career']} - {task['title']}: {task['description']}"
                else:
                    description = task['description']
                
                f.write(f"TASK|{description}|{task['date']}|{task['status']}\n")
    
    def update_task_list(self):
        """Refresh the task table with filtered and sorted tasks."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        if not self.filtered_tasks:
            # Add a placeholder row when no tasks are found
            self.task_tree.insert("", "end", values=("No tasks found", "", "", "", ""), tags=("oddrow",))
            return
        
        # Sort tasks by date
        sorted_tasks = sorted(self.filtered_tasks, key=lambda t: t["date"])
        
        # Add tasks to the table
        for i, task in enumerate(sorted_tasks):
            status = "✓" if task["status"] == "completed" else "○"
            tags = ("evenrow" if i % 2 == 0 else "oddrow",)
            if task["status"] == "completed":
                tags = tags + ("completed",)
            else:
                tags = tags + ("pending",)
            
            self.task_tree.insert(
                "", 
                "end", 
                values=(status, task["date"], task["career"], task["title"], task["description"]),
                tags=tags
            )
    
    def _get_selected_task_from_tree(self):
        """Helper to get the full task dictionary from the current tree selection."""
        selected_items = self.task_tree.selection()
        if not selected_items:
            return None
            
        selected_item = selected_items[0]
        values = self.task_tree.item(selected_item, "values")
        
        # Skip if it's the "No tasks found" message
        if values[0] == "No tasks found":
            return None
        
        try:
            # Extract values from the selected row
            status = values[0]
            task_date_str = values[1]
            career = values[2]
            title = values[3]
            description = values[4]

            # Find the task in our main list using the parsed values
            for task in self.tasks:
                if (task["date"] == task_date_str and 
                    task["career"] == career and 
                    task["title"] == title and 
                    task["description"] == description):
                    return task
        except (IndexError, KeyError):
            # This can happen if the display format is unexpected
            print(f"DEBUG: Parsing failed for values: {values}") # Debug print
            messagebox.showerror("Error", f"Could not parse the selected task.\nValues: {values}")
            return None
            
        return None

    def mark_complete(self):
        """Toggle the 'completed' status of the selected task."""
        task = self._get_selected_task_from_tree()
        if not task:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")
            return
            
        # Toggle task status
        task["status"] = "completed" if task["status"] == "pending" else "pending"
        self.save_tasks()
        self.apply_filters(self.current_date_filter, self.current_career_filter)
    
    def delete_task(self):
        """Delete the selected task after confirmation."""
        task = self._get_selected_task_from_tree()
        if not task:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return
            
        # Confirm deletion with user
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this task?\n\n'{task['title']}: {task['description']}'"):
            self.tasks.remove(task)
            self.save_tasks()
            self.apply_filters(self.current_date_filter, self.current_career_filter)