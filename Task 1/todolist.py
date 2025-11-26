# To-Do List App with Tkinter
# Developed by: Akansh Jadam
# Internship Task - CodSoft (Python Programming Internship)
# Date: 26/NOV/2025


import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class TASK1:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Color scheme
        self.bg_color = "#053668"
        self.primary_color = "#1d252d"
        self.danger_color = "#a31510"
        
        self.root.configure(bg=self.bg_color)
        
        # Data file
        self.data_file = "tasks.json"
        self.tasks = []
        self.load_tasks()
        
        # Setup GUI
        self.setup_gui()
        self.refresh_task_list()
        
    def setup_gui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="To-Do List", 
            font=("Arial", 20, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Task Entry
        self.task_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=45,
            relief=tk.FLAT,
            bg="white",
            fg="#333"
        )
        self.task_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Add Button
        add_btn = tk.Button(
            input_frame,
            text="Add Task",
            font=("Arial", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task,
            padx=20,
            pady=8
        )
        add_btn.pack(side=tk.LEFT)
        
        # Task List Frame with Scrollbar
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(
            list_frame,
            bg="white",
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Frame inside canvas
        self.task_list_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.task_list_frame,
            anchor="nw"
        )
        
        self.task_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Bind canvas width to frame width
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        clear_completed_btn = tk.Button(
            button_frame,
            text="Clear Completed",
            font=("Arial", 10, "bold"),
            bg="#5cb85c",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_completed,
            padx=15,
            pady=8
        )
        clear_completed_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_all_btn = tk.Button(
            button_frame,
            text="Delete All",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.delete_all,
            padx=15,
            pady=8
        )
        delete_all_btn.pack(side=tk.LEFT)
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        task = {
            "id": datetime.now().timestamp(),
            "text": task_text,
            "completed": False
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.refresh_task_list()
        
    def toggle_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.save_tasks()
        self.refresh_task_list()
        
    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
        self.refresh_task_list()
        
    def clear_completed(self):
        completed_count = sum(1 for task in self.tasks if task["completed"])
        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
        
        if messagebox.askyesno("Confirm", f"Clear {completed_count} completed task(s)?"):
            self.tasks = [task for task in self.tasks if not task["completed"]]
            self.save_tasks()
            self.refresh_task_list()
            
    def delete_all(self):
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Delete all tasks?"):
            self.tasks = []
            self.save_tasks()
            self.refresh_task_list()
            
    def refresh_task_list(self):
        # Clear existing widgets
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        # Display tasks
        if not self.tasks:
            no_task_label = tk.Label(
                self.task_list_frame,
                text="No tasks yet. Add one above!",
                font=("Arial", 12),
                bg="white",
                fg="#999"
            )
            no_task_label.pack(pady=50)
        else:
            for task in self.tasks:
                self.create_task_widget(task)
                
    def create_task_widget(self, task):
        # Task frame
        task_frame = tk.Frame(
            self.task_list_frame,
            bg="#f9f9f9",
            relief=tk.FLAT,
            bd=1,
            highlightbackground="#ddd",
            highlightthickness=1
        )
        task_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Content frame
        content_frame = tk.Frame(task_frame, bg="#f9f9f9")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Checkbox
        check_var = tk.BooleanVar(value=task["completed"])
        checkbox = tk.Checkbutton(
            content_frame,
            variable=check_var,
            command=lambda: self.toggle_task(task["id"]),
            bg="#f9f9f9",
            activebackground="#f9f9f9",
            cursor="hand2"
        )
        checkbox.pack(side=tk.LEFT, padx=(0, 10))
        
        # Task text
        task_label = tk.Label(
            content_frame,
            text=task["text"],
            font=("Arial", 11, "overstrike" if task["completed"] else "normal"),
            bg="#f9f9f9",
            fg="#999" if task["completed"] else "#333",
            anchor="w",
            justify=tk.LEFT,
            wraplength=420
        )
        task_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Delete button
        delete_btn = tk.Button(
            content_frame,
            text="Delete",
            font=("Arial", 9),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.delete_task(task["id"]),
            padx=10,
            pady=4
        )
        delete_btn.pack(side=tk.RIGHT)
        
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []
            
    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

def main():
    root = tk.Tk()
    app = TASK1(root)
    root.mainloop()

if __name__ == "__main__":
    main()