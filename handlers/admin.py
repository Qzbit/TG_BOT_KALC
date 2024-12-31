from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.db_utils import get_all_users, update_text_description, add_user
from database.db_utils import get_all_users


import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Список ID администраторов
ADMINS = [1189522582]

from database.db_utils import get_all_users

from database.db_utils import get_all_users

def list_all_users():
    """Пример использования функции get_all_users."""
    users = get_all_users()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Status: {user[2]}, Subscription Ends: {user[3]}")



def register_handlers(bot):
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        """Отображает главное меню админ-панели."""
        if message.chat.id in ADMINS:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton("Просмотр пользователей"))
            keyboard.add(KeyboardButton("Изменить текст описания"))
            keyboard.add(KeyboardButton("Добавить пользователя"))
            bot.send_message(
                message.chat.id,
                "⚙️ Добро пожаловать в панель администратора. Выберите действие:",
                reply_markup=keyboard
            )
            logger.info(f"Администратор {message.chat.id} открыл панель администратора.")
        else:
            bot.send_message(message.chat.id, "❌ У вас нет доступа к этой команде.")
            logger.warning(f"Пользователь {message.chat.id} пытался получить доступ к админ-панели.")

    @bot.message_handler(func=lambda message: message.text == "Просмотр пользователей")
    def view_users(message):
        """Отображает список зарегистрированных пользователей."""
        if message.chat.id in ADMINS:
            try:
                users = get_all_users()
                if not users:
                    bot.send_message(message.chat.id, "📃 Нет зарегистрированных пользователей.")
                else:
                    response = "📃 Список пользователей:\n"
                    for user in users:
                        username = user.get("username", "Не указан")  # Проверяем, есть ли никнейм
                        response += f"ID: {user['id']}, Ник: {username}, Статус: {user['status']}, Подписка до: {user['subscription_end']}\n"
                    bot.send_message(message.chat.id, response)
                    logger.info("Администратор запросил список пользователей.")
            except Exception as e:
                bot.send_message(message.chat.id, "❌ Ошибка при получении списка пользователей.")
                logger.error(f"Ошибка при просмотре пользователей: {e}")
        else:
            bot.send_message(message.chat.id, "❌ У вас нет доступа к этой функции.")

    @bot.message_handler(func=lambda message: message.text == "Изменить текст описания")
    def edit_description_prompt(message):
        """Выводит инструкцию для изменения текста описания."""
        if message.chat.id in ADMINS:
            bot.send_message(message.chat.id, "Введите команду в формате: /update_text <идентификатор> <новый текст>")
        else:
            bot.send_message(message.chat.id, "❌ У вас нет доступа к этой функции.")

    @bot.message_handler(commands=['update_text'])
    def update_text_command(message):
        """Обновляет текст описания в базе данных."""
        if message.chat.id in ADMINS:
            try:
                parts = message.text.split(' ', 2)
                if len(parts) < 3:
                    raise ValueError("Недостаточно данных.")
                identifier, new_text = parts[1], parts[2]
                update_text_description(identifier, new_text)
                bot.send_message(message.chat.id, f"✅ Текст для '{identifier}' успешно обновлен.")
                logger.info(f"Администратор обновил текст для '{identifier}'.")
            except ValueError:
                bot.send_message(message.chat.id, "❌ Ошибка! Используйте формат: /update_text <идентификатор> <новый текст>")
            except Exception as e:
                bot.send_message(message.chat.id, "❌ Ошибка при обновлении текста.")
                logger.error(f"Ошибка в 'update_text_command': {e}")
        else:
            bot.send_message(message.chat.id, "❌ У вас нет доступа к этой команде.")

    @bot.message_handler(func=lambda message: message.text == "Добавить пользователя")
    def add_user_prompt(message):
        """Выводит инструкцию для добавления нового пользователя."""
        if message.chat.id in ADMINS:
            bot.send_message(message.chat.id, "Введите данные пользователя в формате: /add_user <ID> <Статус> <Дата окончания подписки (ДД-ММ-ГГГГ)>")
        else:
            bot.send_message(message.chat.id, "❌ У вас нет доступа к этой функции.")

    @bot.message_handler(commands=['add_user'])
    def add_user_command(message):
        """Добавляет нового пользователя в базу данных."""
        if message.chat.id in ADMINS:
            try:
                parts = message.text.split(' ', 3)
                if len(parts) < 4:
                    raise ValueError("Недостаточно данных.")
                user_id, status, subscription_end = parts[1], parts[2], parts[3]
                add_user(user_id, status, subscription_end)
                bot.send_message(message.chat.id, f"✅ Пользователь с ID {user_id} успешно добавлен.")
                logger.info(f"Администратор добавил пользователя с ID {user_id}.")
            except ValueError:
                bot.send_message(message.chat.id, "❌ Ошибка! Используйте формат: /add_user <ID> <Статус> <Дата окончания подписки (ДД-ММ-ГГГГ)>")
            except Exception as e:
                bot.send_message(message.chat.id, "❌ Ошибка при добавлении пользователя.")
                logger.error(f"Ошибка в 'add_user_command': {e}")
        else:
            bot.send_message(message.chat.id, "❌ У вас нет доступа к этой команде.")
