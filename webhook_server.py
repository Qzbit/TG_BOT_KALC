from flask import Flask
from handlers.payment import payment_bp

# Инициализация приложения Flask
app = Flask(__name__)

# Регистрация Blueprint для маршрутов, связанных с платежами
app.register_blueprint(payment_bp, url_prefix='/payment')

if __name__ == "__main__":
    # Запуск приложения
    app.run(host="0.0.0.0", port=80)  # Слушаем порт 80
