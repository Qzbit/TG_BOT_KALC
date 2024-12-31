# calculators/wealth_number.py

def calculate_wealth_number(number: int, fullname: str) -> int:
    """Рассчитывает число богатства."""
    def get_sum_of_digits(num):
        while num > 9:
            num = sum(int(digit) for digit in str(num))
        return num

    def get_name_value(name):
        char_map = {
            'А': 1, 'И': 1, 'С': 1, 'Ъ': 1,
            'Б': 2, 'Й': 2, 'Т': 2, 'Ы': 2,
            'В': 3, 'К': 3, 'У': 3, 'Ь': 3,
            'Г': 4, 'Л': 4, 'Ф': 4, 'Э': 4,
            'Д': 5, 'М': 5, 'Х': 5, 'Ю': 5,
            'Е': 6, 'Н': 6, 'Ц': 6, 'Я': 6,
            'Ё': 7, 'О': 7, 'Ч': 7,
            'Ж': 8, 'П': 8, 'Ш': 8,
            'З': 9, 'Р': 9, 'Щ': 9
        }
        return sum(char_map.get(char.upper(), 0) for char in name)

    number_sum = get_sum_of_digits(int(number))
    name_sum = get_sum_of_digits(get_name_value(fullname))
    wealth_number = get_sum_of_digits(number_sum + name_sum)
    return wealth_number


import json
import os

# Путь к файлу описаний
WEALTH_DESCRIPTIONS_PATH = os.path.join("templates", "descriptions", "wealth.json")

def calculate_wealth_number(number: int, fullname: str) -> int:
    """Рассчитывает число богатства."""
    def get_sum_of_digits(num):
        while num > 9:
            num = sum(int(digit) for digit in str(num))
        return num

    def get_name_value(name):
        char_map = {
            'А': 1, 'И': 1, 'С': 1, 'Ъ': 1,
            'Б': 2, 'Й': 2, 'Т': 2, 'Ы': 2,
            'В': 3, 'К': 3, 'У': 3, 'Ь': 3,
            'Г': 4, 'Л': 4, 'Ф': 4, 'Э': 4,
            'Д': 5, 'М': 5, 'Х': 5, 'Ю': 5,
            'Е': 6, 'Н': 6, 'Ц': 6, 'Я': 6,
            'Ё': 7, 'О': 7, 'Ч': 7,
            'Ж': 8, 'П': 8, 'Ш': 8,
            'З': 9, 'Р': 9, 'Щ': 9
        }
        return sum(char_map.get(char.upper(), 0) for char in name)

    number_sum = get_sum_of_digits(int(number))
    name_sum = get_sum_of_digits(get_name_value(fullname))
    wealth_number = get_sum_of_digits(number_sum + name_sum)
    return wealth_number

def get_wealth_description(wealth_number: int) -> str:
    """Возвращает описание для числа богатства из JSON-файла."""
    try:
        with open(WEALTH_DESCRIPTIONS_PATH, "r", encoding="utf-8") as file:
            descriptions = json.load(file)
        return descriptions.get(str(wealth_number), "Описание отсутствует.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при загрузке описаний: {e}")
        return "Ошибка загрузки описаний."
