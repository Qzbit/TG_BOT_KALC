from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_utils import get_referrals

def register_handlers(bot):
    """Регистрирует обработчики для реферальной системы."""

    @bot.message_handler(commands=['referral'])
    def referral_system(message):
        """Обрабатывает команду /referral для управления реферальной системой."""
        user_id = message.chat.id

        # Генерация реферальной ссылки
        referral_link = f"https://t.me/num_calc_bot?start=ref_{user_id}"

        # Получение списка рефералов из базы данных
        referrals = get_referrals(user_id)

        referral_info = "\n".join([f"{ref['username']} ({ref['status']})" for ref in referrals])
        referral_message = (
            f"Ваша реферальная ссылка: {referral_link}\n\n"
            "Поделитесь этой ссылкой с друзьями! Вы получите бонус +1 месяц подписки, если ваш друг активирует подписку.\n\n"
            "Ваши рефералы:\n"
            f"{referral_info if referrals else 'Нет рефералов'}"
        )

        # Клавиатура для возврата в главное меню
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Назад в меню", callback_data="main_menu"))

        bot.send_message(user_id, referral_message, reply_markup=keyboard)
