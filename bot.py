import logging
import signal
import sys
from telebot import TeleBot
from handlers import start, admin, reminders, subscription, referral, star_pythagoras_handler
from database.models import init_db
from config import API_TOKEN

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def initialize_bot():
    """Инициализирует экземпляр бота."""
    try:
        bot_instance = TeleBot(API_TOKEN)
        logger.info("Bot initialized successfully.")
        return bot_instance
    except Exception as e:
        logger.critical(f"Failed to initialize bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Инициализация базы данных
        init_db()
        logger.info("Database initialized successfully.")

        # Создание объекта бота
        bot = initialize_bot()

        # Регистрация обработчиков
        start.register_handlers(bot)
        admin.register_handlers(bot)
        reminders.register_handlers(bot)
        subscription.register_handlers(bot)
        referral.register_handlers(bot)
        star_pythagoras_handler.register_handlers(bot)

        # Запуск бота
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
        logger.info("Bot is running...")
        bot.infinity_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"An unhandled error occurred: {e}")
        sys.exit(1)
