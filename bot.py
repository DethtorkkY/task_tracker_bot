# bot.py
import telebot
from config import TOKEN
from logic import init_db, add_task, get_tasks, delete_task
from telebot import types

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
        task, due_date = message.text.split(' - ')
        add_task(message.from_user.id, task, due_date)
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

# Запуск бота
bot.polling(none_stop=True)
