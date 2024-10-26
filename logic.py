# logic.py
import sqlite3
from config import DATABASE

# Инициализация базы данных (создание таблицы задач)
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Создаем таблицу задач, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task TEXT NOT NULL,
            due_date TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Добавление новой задачи
def add_task(user_id, task, due_date):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (user_id, task, due_date) 
        VALUES (?, ?, ?)
    ''', (user_id, task, due_date))
    
    conn.commit()
    conn.close()

# Получение списка задач пользователя
def get_tasks(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT task, due_date FROM tasks WHERE user_id = ?
    ''', (user_id,))
    
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks

# Удаление задачи по ее названию
def delete_task(user_id, task):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM tasks WHERE user_id = ? AND task = ?
    ''', (user_id, task))
    
    conn.commit()
    conn.close()
