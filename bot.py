
import telebot
from config import TOKEN
from logic import init_db, add_task, get_tasks, delete_task, get_all_user_ids
from telebot import types
from datetime import datetime
import threading
import time

# Инициализация бота с использованием токена
bot = telebot.TeleBot(TOKEN)

# Инициализация базы данных при запуске бота
init_db()

# Команда /start - Приветствие пользователя
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Привет! Я помогу тебе отслеживать задачи. Вот мои команды:\n"
        "/add - Добавить задачу\n"
        "/list - Показать задачи\n"
        "/delete - Удалить задачу"
    )

# Обработка команды /add для добавления задачи
@bot.message_handler(commands=['add'])
def add(message):
    msg = bot.send_message(message.chat.id, "Введите задачу и дату в формате: Задача - Дата (YYYY-MM-DD)")
    bot.register_next_step_handler(msg, process_task_step)

# Функция обработки добавления задачи
def process_task_step(message):
    try:
        # Разделяем ввод пользователя на задачу и дату
        task, due_date_str = message.text.split(' - ')
        
        # Преобразуем введенную строку в объект даты
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = datetime.today().date()

        # Проверяем, является ли дата сегодня или в будущем
        if due_date < today:
            bot.send_message(message.chat.id, "Ошибка: Нельзя указать прошедшую дату. Попробуйте снова.")
        else:
            add_task(message.from_user.id, task, due_date_str)
            bot.send_message(message.chat.id, "Задача добавлена!")
    
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный формат! Используйте: Задача - Дата (YYYY-MM-DD)")

# Обработка команды /list для отображения списка задач
@bot.message_handler(commands=['list'])
def list_tasks(message):
    tasks = get_tasks(message.from_user.id)
    if tasks:
        response = "Ваши задачи:\n" + "\n".join([f"{task} - {due_date}" for task, due_date in tasks])
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "У вас нет задач.")

# Обработка команды /delete для удаления задачи
@bot.message_handler(commands=['delete'])
def delete(message):
    msg = bot.send_message(message.chat.id, "Введите название задачи для удаления:")
    bot.register_next_step_handler(msg, process_delete_task)

# Функция обработки удаления задачи
def process_delete_task(message):
    task = message.text
    delete_task(message.from_user.id, task)
    bot.send_message(message.chat.id, "Задача удалена!")

# Функция для отправки уведомлений о задачах на сегодня
def send_task_notifications():
    while True:
        # Получаем текущую дату
        today = datetime.today().date()

        # Для всех пользователей проверяем задачи на сегодня
        for user_id in get_all_user_ids():  # Получаем всех пользователей, которые добавляли задачи
            tasks = get_tasks(user_id)
            today_tasks = [task for task, due_date in tasks if due_date == today.strftime('%Y-%m-%d')]

            # Отправляем уведомления, если есть задачи на сегодня
            if today_tasks:
                task_list = "\n".join(today_tasks)
                bot.send_message(user_id, f"Напоминание! На сегодня у вас есть следующие задачи:\n{task_list}")

        # Ждем 30 минут перед следующей проверкой
        time.sleep(1500)

# Запуск потока для отправки уведомлений
notification_thread = threading.Thread(target=send_task_notifications)
notification_thread.start()

# Запуск бота
bot.polling(none_stop=True)
