import logging
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_utils import add_user, is_subscription_active, get_subscription_status
from calculators.arcanum_number import calculate_arcanum_number, get_arcanum_description
from handlers.payment import create_payment
import re

logger = logging.getLogger(__name__)

def is_valid_date(date_str):
    """Проверяет, соответствует ли строка формату даты ДД.ММ.ГГГГ."""
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def register_handlers(bot):
    """Регистрирует обработчики для стартовых команд и меню."""

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """Приветственное сообщение при команде /start."""
        try:
            user_id = message.chat.id
            username = message.from_user.username or "Anonymous"
            status = "inactive"
            subscription_end = "1970-01-01"

            add_user(user_id, username, status, subscription_end)

            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton("Калькуляторы", callback_data="calculators"),
                InlineKeyboardButton("Подписка", callback_data="subscribe"),
                InlineKeyboardButton("Напоминания", callback_data="reminders")
            )

            bot.send_message(
                message.chat.id,
                (
                    f"Добро пожаловать {username} в Матрицу чисел! 🌌\n\n"
                    "Откройте для себя значение чисел и их влияние на вашу жизнь. Наш бот поможет вам рассчитать:\n"
                    "🔢 Число жизненного пути\n"
                    "🃏 Арканы по дате рождения (доступно бесплатно)\n"
                    "⭐️ Звезду Пифагора и многое другое.\n\n"
                    "Выберите интересующий вас раздел из меню ниже. 🚀"
                ),
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка в 'send_welcome': {e}")
            bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте позже.")

    @bot.callback_query_handler(func=lambda call: call.data == "calculators")
    def show_calculators(call):
        """Показывает меню калькуляторов."""
        try:
            user_id = call.message.chat.id
            subscription_status, subscription_end = get_subscription_status(user_id)
            has_active_subscription = is_subscription_active(subscription_end)

            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton("Число арканов", callback_data="arcanum_number")
            )

            if has_active_subscription:
                keyboard.add(
                    InlineKeyboardButton("Число личного дня", callback_data="personal_day"),
                    InlineKeyboardButton("Звезда Пифагора", callback_data="pythagoras"),
                    InlineKeyboardButton("Число богатства", callback_data="wealth")
                )
            else:
                keyboard.add(
                    InlineKeyboardButton("Подписаться", callback_data="subscribe")
                )

            keyboard.add(
                InlineKeyboardButton("Назад", callback_data="main_menu")
            )

            bot.edit_message_text(
                "Воспользуйтесь нашим презентационным калькулятором.\n"
                "Для доступа ко всем калькуляторам оформите подписку.",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка в 'show_calculators': {e}")
            bot.send_message(call.message.chat.id, "Произошла ошибка. Попробуйте позже.")

    @bot.callback_query_handler(func=lambda call: call.data == "main_menu")
    def show_main_menu(call):
        """Возвращает пользователя в стартовое меню."""
        try:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton("Калькуляторы", callback_data="calculators"),
                InlineKeyboardButton("Подписка", callback_data="subscribe"),
                InlineKeyboardButton("Напоминания", callback_data="reminders")
            )

            bot.edit_message_text(
                (
                    "Добро пожаловать в Матрицу чисел! 🌌\n\n"
                    "Выберите интересующий вас раздел из меню ниже. 🚀"
                ),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка в 'show_main_menu': {e}")
            bot.send_message(call.message.chat.id, "Произошла ошибка. Попробуйте позже.")

    @bot.callback_query_handler(func=lambda call: call.data == "arcanum_number")
    def handle_arcanum(call):
        """Обрабатывает выбор 'Число арканов'."""
        try:
            bot.send_message(call.message.chat.id, "Введите вашу дату рождения в формате ДД.ММ.ГГГГ:")
            bot.register_next_step_handler(call.message, process_arcanum)
        except Exception as e:
            logger.error(f"Ошибка в 'handle_arcanum': {e}")
            bot.send_message(call.message.chat.id, "Произошла ошибка. Попробуйте позже.")

    def process_arcanum(message):
        """Обрабатывает ввод для числа арканов."""
        try:
            birth_date = message.text.strip()
            if not is_valid_date(birth_date):
                bot.send_message(message.chat.id, "Ошибка! Введите дату в формате ДД.ММ.ГГГГ.")
                return

            arcanum_number = calculate_arcanum_number(birth_date)
            arcanum_description = get_arcanum_description(arcanum_number)

            bot.send_message(
                message.chat.id,
                f"Ваше число арканов: {arcanum_number}\n\n"
                f"Описание: {arcanum_description}"
            )
        except Exception as e:
            logger.error(f"Ошибка в 'process_arcanum': {e}")
            bot.send_message(message.chat.id, "Произошла ошибка при расчёте числа арканов. Попробуйте позже.")
