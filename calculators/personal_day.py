import json
from datetime import datetime

def calculate_personal_day(birth_date: str) -> int:
    """
    Рассчитывает Число личного дня на основе даты рождения (без года) и текущей даты.
    """
    try:
        # Проверяем формат даты
        birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
        today = datetime.today()

        # Суммируем текущую дату
        current_date_sum = sum(map(int, today.strftime("%d%m%Y")))

        # Суммируем день и месяц даты рождения (год исключается)
        birth_date_sum = sum(map(int, birth_date.strftime("%d%m")))  # Только день и месяц

        # Рассчитываем Число личного дня
        personal_day_number = (birth_date_sum + current_date_sum) % 9
        return personal_day_number if personal_day_number != 0 else 9
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте формат: ДД.ММ.ГГГГ")

def get_personal_day_description(personal_day: int) -> str:
    """
    Возвращает описание числа личного дня.
    """
    # Попробуйте использовать JSON файл, если он есть
    try:
        with open("templates/descriptions/personal_day.json", "r", encoding="utf-8") as file:
            descriptions = json.load(file)
        return descriptions.get(str(personal_day), "Описание отсутствует.")
    except FileNotFoundError:
        # Если файл не найден, возвращаем описание из словаря
        descriptions = {
            1: "Число 1 — день новых начинаний, лидерства и активных действий.",
            2: "Число 2 — день гармонии и партнёрства. Подходит для общения и сотрудничества.",
            3: "Число 3 — день творчества, самовыражения и общения.",
            4: "Число 4 — день стабильности и упорного труда.",
            5: "Число 5 — день перемен и приключений.",
            6: "Число 6 — день заботы, ответственности и семейных отношений.",
            7: "Число 7 — день размышлений, анализа и духовного роста.",
            8: "Число 8 — день амбиций, успеха и достижения целей.",
            9: "Число 9 — день завершений, благотворительности и мудрости."
        }
        return descriptions.get(personal_day, "Описание отсутствует.")
