from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database.db_utils import get_subscription_status, update_subscription
from yookassa import Payment, Configuration

# Настройка конфигурации ЮKassa
Configuration.account_id = "85D187ACD8A87A90B3B38EB3E7DF908F0CEE92AAADB77F5869E4BDDCDCB9AF46"
Configuration.secret_key = "2F6DE94B3DAA9FAD8E4DA8F6A2864B13C04274EEB6EBF93A1971AEF4108A5C13EBDC82ABF451F9A5A42166BC5ACBC84232ECABB5951DCB48D8EDE74A3EC0E3A8"


def create_payment_url(amount=1.0, currency="RUB", description="Подписка на 1 месяц"):
    """Создание ссылки на оплату через ЮKassa."""
    payment = Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": currency
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://194.87.133.76:80/payment/success"
        },
        "capture": True,
        "description": description
    })
    return payment.confirmation.confirmation_url


def register_handlers(bot):
    @bot.message_handler(commands=['subscription'])
    def manage_subscription(message):
        """Обрабатывает команду /subscription для проверки статуса подписки."""
        user_id = message.chat.id

        try:
            user_status, expiry_date = get_subscription_status(user_id)

            if user_status == "active":
                bot.send_message(
                    user_id,
                    f"Ваша подписка активна до {expiry_date.strftime('%d.%m.%Y')}."
                )
            else:
                keyboard = InlineKeyboardMarkup()
                extend_button = InlineKeyboardButton(
                    "Продлить подписку за 1 рубль", callback_data="extend_subscription"
                )
                keyboard.add(extend_button)

                bot.send_message(
                    user_id,
                    "Ваша подписка истекла. Продлите её для доступа ко всем функциям.",
                    reply_markup=keyboard
                )
        except Exception as e:
            bot.send_message(user_id, f"Произошла ошибка при проверке подписки: {e}")

    @bot.callback_query_handler(func=lambda call: call.data == "extend_subscription")
    def extend_subscription(call):
        """Создает ссылку на оплату подписки через ЮKassa."""
        try:
            payment_url = create_payment_url(amount=1.0)  # Сумма подписки: 1 рубль
            markup = InlineKeyboardMarkup()
            pay_button = InlineKeyboardButton("Оплатить 1 рубль", url=payment_url)
            markup.add(pay_button)

            bot.send_message(
                call.message.chat.id,
                "Для активации подписки на 1 месяц, пожалуйста, оплатите 1 рубль.",
                reply_markup=markup
            )
        except Exception as e:
            bot.send_message(
                call.message.chat.id,
                f"Произошла ошибка при создании платежа: {e}"
            )

    @bot.message_handler(func=lambda message: message.text == "Продлить подписку")
    def manual_extend_subscription(message):
        """Ручное продление подписки (альтернатива кнопке)."""
        try:
            user_id = message.chat.id
            new_expiry_date = datetime.now() + timedelta(days=30)
            update_subscription(user_id, new_expiry_date)

            bot.send_message(
                user_id,
                f"Подписка успешно продлена до {new_expiry_date.strftime('%Y-%m-%d')}."
            )
        except Exception as e:
            bot.send_message(user_id, f"Произошла ошибка при продлении подписки: {e}")
