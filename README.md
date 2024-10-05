# Task Tracker Bot

Простой Telegram-бот для отслеживания задач с использованием базы данных.

## Инструменты для реализации:
- Язык программирования: Python
- Telegram Bot API
- База данных: SQLite
- Библиотеки: 
  - `python-telegram-bot-api` для взаимодействия с Telegram API
  - `SQLite3` для работы с базой данных
  - `dotenv` для работы с переменными окружения

## Проект состоит из:
1. **Регистрация пользователя** - Пользователи могут регистрироваться и их данные будут сохраняться в базе данных.
2. **Добавление задачи** - Возможность добавления задачи с указанием её описания.
3. **Просмотр текущих задач** - Вывод списка активных задач для пользователя.
4. **Завершение задачи** - Пометка задачи как выполненной.
5. **Удаление задачи** - Возможность удаления задачи из списка.
6. **История выполненных задач** - Просмотр завершённых задач.
7. **Напоминания (опционально)** - Настройка напоминаний для невыполненных задач.