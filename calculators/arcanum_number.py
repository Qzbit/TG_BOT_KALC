import json

def calculate_arcanum_number(birth_date: str) -> int:
    """
    Рассчитывает число арканы на основе даты рождения.
    """
    try:
        digits_sum = sum(int(digit) for digit in birth_date if digit.isdigit())
        while digits_sum > 22:
            digits_sum = sum(int(digit) for digit in str(digits_sum))
        return digits_sum
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте формат: ДД.ММ.ГГГГ")

def get_arcanum_description(arcanum_number: int) -> str:
    """
    Возвращает описание числа арканы.
    """
    try:
        with open("templates/descriptions/arcanum.json", "r", encoding="utf-8") as file:
            descriptions = json.load(file)
        return descriptions.get(str(arcanum_number), "Описание отсутствует.")
    except FileNotFoundError:
        return "Файл с описаниями арканов не найден."
