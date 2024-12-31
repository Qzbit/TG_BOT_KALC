import json
from flask import Blueprint, request, jsonify
from database.db_utils import update_subscription_status
from yookassa import Configuration, Payment

# Настройка конфигурации ЮKassa
Configuration.account_id = "85D187ACD8A87A90B3B38EB3E7DF908F0CEE92AAADB77F5869E4BDDCDCB9AF46"
Configuration.secret_key = "2F6DE94B3DAA9FAD8E4DA8F6A2864B13C04274EEB6EBF93A1971AEF4108A5C13EBDC82ABF451F9A5A42166BC5ACBC84232ECABB5951DCB48D8EDE74A3EC0E3A8"

# Создаем Blueprint для маршрутов, связанных с платежами
payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/redirect_uri', methods=['GET', 'POST'])
def handle_redirect():
    """Обработка Redirect URI."""
    data = request.args if request.method == 'GET' else request.json
    order_id = data.get('order_id')
    status = data.get('status')

    if status == "success":
        print(f"Платеж {order_id} прошел успешно.")
        update_subscription_status(order_id, status="active")
        return "Оплата успешно обработана. Спасибо!", 200
    else:
        print(f"Платеж {order_id} завершился с ошибкой.")
        return "Ошибка при обработке оплаты. Пожалуйста, попробуйте позже.", 400

@payment_bp.route('/notification_uri', methods=['POST'])
def handle_notification():
    """Обработка Notification URI."""
    if not request.is_json:
        return jsonify({"error": "Invalid request format. JSON expected."}), 400

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Malformed JSON"}), 400

    payment_id = data.get('object', {}).get('id')
    status = data.get('object', {}).get('status')

    if not payment_id or not status:
        return jsonify({"error": "Missing required fields in JSON"}), 400

    if status == "succeeded":
        print(f"Платеж {payment_id} успешно завершен.")
        update_subscription_status(payment_id, status="active")
    elif status == "canceled":
        print(f"Платеж {payment_id} был отменен.")
        update_subscription_status(payment_id, status="canceled")

    return jsonify({"status": "processed"}), 200

def create_payment(amount, currency="RUB", description="Оплата услуги"):
    """Создание платежа в ЮKassa."""
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
    return payment

def handle_payment_notification(data):
    """Обработка уведомления о платеже."""
    payment_id = data.get("object", {}).get("id")
    status = data.get("object", {}).get("status")

    if status == "succeeded":
        print(f"Платеж {payment_id} успешно завершён")
    elif status == "canceled":
        print(f"Платеж {payment_id} отменён")
    return jsonify({"status": "ok"}), 200
