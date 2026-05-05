import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Настройки
HISTORY_FILE = "tasks.json"
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Посмотреть обучающее видео", "type": "учёба"},
    {"text": "Разобрать почту", "type": "работа"},
    {"text": "Погулять на свежем воздухе", "type": "отдых"},
]


class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x500")
        # Загрузка данных
        self.tasks = self.load_tasks()
        # Текущая задача
        self.current_task_label = tk.Label(
            root, text="Нажмите 'Сгенерировать задачу'",
            wraplength=400, justify="center", font=("Arial", 12)
        )
        self.current_task_label.pack(pady=10)
        # Кнопка генерации
        self.generate_btn = tk.Button(
            root, text="Сгенерировать задачу", command=self.generate_task,
            bg="#4CAF50", fg="white", font=("Arial", 10)
        )
        self.generate_btn.pack(pady=5)
        # Фильтрация
        filter_frame = tk.Frame(root)
        filter_frame.pack(fill=tk.X, pady=5)
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        filter_options = ["Все", "учёба", "спорт", "работа", "отдых"]
        filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly")
        filter_menu.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        filter_menu.bind("<<ComboboxSelected>>", self.update_history_list)
        # История
        history_frame = tk.Frame(root)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.history_listbox = tk.Listbox(history_frame, height=10)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
        # Добавление новой задачи
        add_frame = tk.Frame(root)
        add_frame.pack(fill=tk.X, pady=5)
        tk.Label(add_frame, text="Новая задача:").pack(side=tk.LEFT)
        self.new_task_entry = tk.Entry(add_frame, width=30)
        self.new_task_entry.pack(side=tk.LEFT, expand=True)
        self.add_btn = tk.Button(add_frame, text="Добавить", command=self.add_new_task)
        self.add_btn.pack(side=tk.RIGHT)
        # Типы задач
        type_frame = tk.Frame(add_frame)
        type_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(type_frame, text="Тип:").pack(side=tk.LEFT)
        self.task_type_var = tk.StringVar(value="учёба")
        type_options = ["учёба", "спорт", "работа", "отдых"]
        type_menu = ttk.Combobox(type_frame, textvariable=self.task_type_var, values=type_options, state="readonly")
        type_menu.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.update_history_list()

    def load_tasks(self):
        """Загрузка задач из JSON или возврат дефолтных."""
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return DEFAULT_TASKS.copy()

    def save_tasks(self):
        """Сохранение задач в JSON."""
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def update_history_list(self, *args):
        """Обновление списка истории с учётом фильтра."""
        self.history_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()
        for task in self.tasks:
            if filter_type == "Все" or task['type'] == filter_type:
                self.history_listbox.insert(tk.END, f"{task['text']} ({task['type']})")
    def generate_task(self):
        """Генерация случайной задачи."""
        if not self.tasks:
            messagebox.showwarning("Предупреждение", "Список задач пуст! Добавьте новые задачи.")
            return
        selected_task = random.choice(self.tasks)
        # Отображаем задачу в главном лейбле
        self.current_task_label.config(
            text=f"Задача: {selected_task['text']}\nТип: {selected_task['type'].capitalize()}",
            bg="#f0f0f0", relief="solid"
        )
    def add_new_task(self):
        """Добавление новой задачи с валидацией."""
        task_text = self.new_task_entry.get().strip()
        task_type = self.task_type_var.get()
        if not task_text:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return
        new_task = {"text": task_text, "type": task_type}
        self.tasks.append(new_task)
        self.save_tasks()
        self.update_history_list()
        self.new_task_entry.delete(0, tk.END)
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()


