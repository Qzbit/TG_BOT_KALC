import sqlite3
import logging
import os

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация базы данных
DB_PATH = os.getenv("DB_PATH", "database/bot_database.db")

# Создание подключения к базе данных
def get_connection():
    """
    Возвращает подключение к базе данных.
    Если подключение невозможно, выбрасывается исключение.
    """
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        logger.critical(f"Ошибка подключения к базе данных: {e}")
        raise SystemExit("Не удалось подключиться к базе данных.")

# Инициализация базы данных
def init_db():
    """
    Создает таблицы 'users' и 'referrals', если они отсутствуют.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                status TEXT NOT NULL,
                subscription_end DATE,
                referrals_count INTEGER DEFAULT 0,
                reminder_time TEXT,
                username TEXT  -- Поле для никнейма
            )
        ''')
        logger.info("Таблица 'users' инициализирована.")

        # Таблица рефералов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER,
                payment_status TEXT DEFAULT 'unpaid',
                FOREIGN KEY (referrer_id) REFERENCES users (id),
                FOREIGN KEY (referred_id) REFERENCES users (id)
            )
        ''')
        logger.info("Таблица 'referrals' инициализирована.")

        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise
    finally:
        conn.close()

# Функция для выполнения миграции
def migrate_db():
    """
    Проверяет и добавляет недостающие колонки в таблицах.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Проверяем существование колонок в таблице 'users'
        cursor.execute("PRAGMA table_info(users);")
        columns = [column[1] for column in cursor.fetchall()]

        if "reminder_time" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN reminder_time TEXT;")
            logger.info("Колонка 'reminder_time' успешно добавлена.")

        if "username" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN username TEXT;")
            logger.info("Колонка 'username' успешно добавлена.")

        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Ошибка при миграции базы данных: {e}")
        raise
    finally:
        conn.close()

# Точка входа для выполнения инициализации и миграции
if __name__ == "__main__":
    try:
        init_db()
        migrate_db()
        logger.info("Инициализация и миграция базы данных завершена.")
    except Exception as e:
        logger.critical(f"Ошибка при настройке базы данных: {e}")

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            status TEXT,
            subscription_end TEXT
        )
    """)
    conn.commit()
    conn.close()
