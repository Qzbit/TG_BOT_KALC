import sqlite3
import logging
from datetime import datetime, timedelta


def get_referrals(user_id):
    """Возвращает список рефералов для пользователя."""
    conn = sqlite3.connect("/home/ftpworker/ZETA_MATRIX_BOT/database/bot_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT referred_user_id, registration_date
            FROM referrals
            WHERE referrer_user_id = ?
        """, (user_id,))
        referrals = cursor.fetchall()
    finally:
        conn.close()
    
    return referrals



logger = logging.getLogger(__name__)

DB_PATH = "bot_database.db"

def execute_query(query, params=(), fetchone=False, fetchall=False):
    """Выполняет SQL-запрос и возвращает результат."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Ошибка выполнения запроса: {e}")
        return None
    finally:
        conn.close()

def is_subscription_active(subscription_end):
    """Проверяет, активна ли подписка пользователя."""
    if not subscription_end:
        return False
    try:
        if isinstance(subscription_end, int):
            subscription_end = str(subscription_end)
        end_date = datetime.strptime(subscription_end, "%d.%m.%Y")
        return datetime.now() <= end_date
    except ValueError as ve:
        logger.error(f"Ошибка формата даты подписки: {ve}")
        return False

def get_subscription_status(user_id):
    """Возвращает статус и дату окончания подписки пользователя."""
    query = "SELECT status, subscription_end FROM users WHERE id = ?"
    result = execute_query(query, (user_id,), fetchone=True)
    if result:
        status, subscription_end = result
        if isinstance(subscription_end, int):
            subscription_end = str(subscription_end)
        return status, subscription_end
    return "inactive", None

def save_reminder_time(user_id, reminder_time):
    """Сохраняет время напоминания для пользователя."""
    try:
        datetime.strptime(reminder_time, "%H:%M")  # Проверка формата
        query = """
            UPDATE users
            SET reminder_time = ?
            WHERE id = ?
        """
        execute_query(query, (reminder_time, user_id))
        logger.info(f"Время напоминания {reminder_time} сохранено для пользователя {user_id}.")
    except ValueError:
        logger.error(f"Неверный формат времени: {reminder_time}")

def update_subscription(user_id, new_expiry_date):
    """Обновляет дату окончания подписки для указанного пользователя."""
    formatted_date = new_expiry_date.strftime("%d.%m.%Y")
    query = """
        UPDATE users
        SET subscription_end = ?
        WHERE id = ?
    """
    execute_query(query, (formatted_date, user_id))
    logger.info(f"Подписка для пользователя {user_id} обновлена до {formatted_date}.")

def add_user(user_id, username, status, subscription_end):
    """Добавляет нового пользователя в базу данных или обновляет существующего."""
    try:
        query = """
            INSERT INTO users (id, username, status, subscription_end)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                status = excluded.status,
                subscription_end = excluded.subscription_end
        """
        execute_query(query, (user_id, username, status, subscription_end))
        logger.info(f"Пользователь {user_id} добавлен или обновлён.")
    except sqlite3.Error as e:
        logger.error(f"Ошибка при добавлении пользователя {user_id}: {e}")

def get_all_users():
    """Получает список всех пользователей из базы данных."""
    query = "SELECT id, username, status, subscription_end FROM users"
    return execute_query(query, fetchall=True)

def update_text_description(id, new_description):
    """Обновляет текстовое описание в базе данных."""
    query = """
        UPDATE descriptions
        SET text = ?
        WHERE id = ?
    """
    try:
        execute_query(query, (new_description, id))
        logger.info(f"Описание с ID {id} обновлено.")
    except sqlite3.Error as e:
        logger.error(f"Ошибка при обновлении описания: {e}")

def get_reminder_time(user_id):
    """Получает время напоминания для пользователя."""
    query = "SELECT reminder_time FROM users WHERE id = ?"
    result = execute_query(query, (user_id,), fetchone=True)
    if result:
        return result[0]
    return None



def update_subscription_status(payment_id, status):
    try:
        conn = sqlite3.connect("/home/ftpworker/ZETA_MATRIX_BOT/database/bot_database.db")
        cursor = conn.cursor()

        # Если нужно обновлять end_date
        cursor.execute("""
        INSERT INTO subscriptions (payment_id, status, end_date)
        VALUES (?, ?, DATETIME('now', '+30 days')) -- Пример: 30 дней от текущей даты
        ON CONFLICT(payment_id) DO UPDATE SET
            status=excluded.status,
            end_date=excluded.end_date,
            updated_at=CURRENT_TIMESTAMP
        """, (payment_id, status))

        conn.commit()
        print("Статус и дата обновлены успешно")
    except Exception as e:
        print(f"Ошибка при обновлении статуса: {e}")
    finally:
        conn.close()
