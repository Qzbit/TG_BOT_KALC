import sqlite3

def create_tables():
    conn = sqlite3.connect("/home/ftpworker/ZETA_MATRIX_BOT/database/bot_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_id TEXT UNIQUE,
        status TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print("Таблицы успешно созданы!")

# Выполнение функции
if __name__ == "__main__":
    create_tables()
