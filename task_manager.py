import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import csv
import os

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # Colors and styles
        self.bg_color = "#f0f8ff"  # Light blue background
        self.button_color = "#4fa3f7"  # Light blue button color
        self.button_hover = "#3380c9"  # Darker blue for hover effect
        self.completed_color = "#66cc66"  # Light green for completed tasks
        self.pending_color = "#ff6666"  # Light red for pending tasks
        self.in_progress_color = "#ffcc00"  # Light yellow for in-progress tasks

        self.tasks = []

        # Calendar widget
        self.calendar = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=20)

        # Task entry
        self.task_label = tk.Label(self.root, text="Add Task:", bg=self.bg_color, font=("Arial", 12, "bold"))
        self.task_label.pack(pady=10)

        self.task_entry = ttk.Entry(self.root, width=40, font=("Arial", 12))
        self.task_entry.pack(pady=5)

        # Task category dropdown
        self.category_label = tk.Label(self.root, text="Category:", bg=self.bg_color, font=("Arial", 12, "bold"))
        self.category_label.pack(pady=5)

        self.category_var = tk.StringVar(value="General")
        self.category_dropdown = ttk.Combobox(
            self.root, textvariable=self.category_var,
            values=["General", "Grocery","Meat","Clothes","Jewellery", "Catering", "Social Media", "Consultancy", "Transport", "Inventory", "Staff", "Events", "Menu", "Others"],
            font=("Arial", 10)
        )
        self.category_dropdown.pack(pady=5)

        # Buttons
        self.add_button = ttk.Button(self.root, text="Add Task", command=self.add_task, style="TButton")
        self.add_button.pack(pady=10)

        self.view_button = ttk.Button(self.root, text="View Tasks", command=self.view_tasks, style="TButton")
        self.view_button.pack(pady=5)

        self.export_button = ttk.Button(self.root, text="Export Tasks", command=self.export_tasks, style="TButton")
        self.export_button.pack(pady=5)

        # Tasks display area
        self.task_frame = tk.Frame(self.root, bg=self.bg_color)
        self.task_frame.pack(pady=20)

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton",
                             padding=10,
                             font=("Arial", 10, "bold"),
                             background=self.button_color,
                             foreground="#003366")
        self.style.map("TButton", background=[("active", self.button_hover)])

        self.root.configure(bg=self.bg_color)

    def add_task(self):
        date = self.calendar.get_date()
        task = self.task_entry.get().strip()
        category = self.category_var.get()
        if task:
            task_data = {"date": date, "task": task, "category": category, "completed": False, "status": "Pending"}
            self.tasks.append(task_data)
            self.task_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Task '{task}' added for {date}")
        else:
            messagebox.showwarning("Input Error", "Please enter a task!")

    def view_tasks(self):
        date = self.calendar.get_date()
        tasks_on_date = [task for task in self.tasks if task["date"] == date]

        # Clear previous tasks displayed
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # Display new tasks
        if tasks_on_date:
            for idx, task in enumerate(tasks_on_date):
                task_color = self.get_task_color(task["status"])

                task_label = tk.Label(self.task_frame, text=task["task"], font=("Arial", 12), bg=task_color,
                                      anchor="w", width=50)
                task_label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

                # Bind right-click to mark task as done
                task_label.bind("<Button-3>", lambda event, i=idx: self.mark_task_done(i))
        else:
            no_task_label = tk.Label(self.task_frame, text=f"No tasks on {date}.", font=("Arial", 12), bg=self.bg_color)
            no_task_label.pack(pady=10)

    def get_task_color(self, status):
        if status == "Completed":
            return self.completed_color
        elif status == "In Progress":
            return self.in_progress_color
        else:
            return self.pending_color

    def mark_task_done(self, task_index):
        task = self.tasks[task_index]
        if task["status"] == "Pending":
            task["status"] = "Completed"
        elif task["status"] == "In Progress":
            task["status"] = "Completed"
        else:
            task["status"] = "In Progress"

        self.view_tasks()  # Refresh task list to show changes

    def export_tasks(self):
        filename = "tasks.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Task", "Category", "Status"])
            for task in self.tasks:
                writer.writerow([task["date"], task["task"], task["category"], task["status"]])
        messagebox.showinfo("Exported", f"Tasks exported to {os.path.abspath(filename)}")


# Main application entry
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
