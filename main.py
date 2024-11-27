import tkinter as tk
from tkinter import messagebox
import json
import os

# Archivo para guardar tareas
TASKS_FILE = "tasks.json"


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.tasks = []

        # Configuración de la interfaz
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20, padx=20)

        self.task_entry = tk.Entry(self.frame, width=40)
        self.task_entry.grid(row=0, column=0, padx=10)
        self.add_button = tk.Button(self.frame, text="Agregar", command=self.add_task)
        self.add_button.grid(row=0, column=1)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=15, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=1, column=0, columnspan=2, pady=10)

        self.complete_button = tk.Button(self.frame, text="Marcar como completada", command=self.complete_task)
        self.complete_button.grid(row=2, column=0, pady=5)
        self.delete_button = tk.Button(self.frame, text="Eliminar tarea", command=self.delete_task)
        self.delete_button.grid(row=2, column=1, pady=5)

        # Cargar tareas desde el archivo
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.update_task_listbox()
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "La tarea no puede estar vacía.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Error", "Por favor selecciona una tarea para eliminar.")

    def complete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = True
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Error", "Por favor selecciona una tarea para marcar como completada.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = f"[{'X' if task['completed'] else ' '}] {task['task']}"
            self.task_listbox.insert(tk.END, display_text)

    def save_tasks(self):
        with open(TASKS_FILE, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as file:
                self.tasks = json.load(file)
            self.update_task_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
