from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "star_pythagoras_template.png")
OUTPUT_PATH = os.path.join(BASE_DIR, "generated_images", "star_pythagoras_result.png")
FONT_PATH = os.path.join(BASE_DIR, "fonts", "arial.ttf")


logger.info(f"TEMPLATE_PATH: {TEMPLATE_PATH}")
logger.info(f"FONT_PATH: {FONT_PATH}")
logger.info(f"OUTPUT_PATH: {OUTPUT_PATH}")


def calculate_star_pythagoras(day, month, year):
    """Выполняет расчёты для Звезды Пифагора."""
    def reduce_to_single_digit(num):
        while num > 9:
            num = sum(int(d) for d in str(num))
        return num

    day_number = reduce_to_single_digit(day)
    month_number = reduce_to_single_digit(month)
    year_number = reduce_to_single_digit(sum(int(d) for d in str(year)))
    sum1 = reduce_to_single_digit(day_number + month_number + year_number)
    sum2 = reduce_to_single_digit(day_number + month_number + year_number + sum1)
    center = reduce_to_single_digit(day_number + month_number + year_number + sum1 + sum2)

    return {
        "day": day_number,
        "month": month_number,
        "year": year_number,
        "sum1": sum1,
        "sum2": sum2,
        "center": center,
    }

def handle_star_pythagoras(birth_date: str) -> str:
    """Выполняет расчёт Звезды Пифагора и создаёт изображение."""
    try:
        parsed_date = datetime.strptime(birth_date, "%d.%m.%Y")
        results = calculate_star_pythagoras(parsed_date.day, parsed_date.month, parsed_date.year)
        image_path = generate_star_image(results)
        return image_path
    except ValueError:
        raise ValueError("Некорректный формат даты. Используйте формат ДД.ММ.ГГГГ.")

def generate_star_image(results):
    """Генерирует изображение Звезды Пифагора с рассчитанными значениями."""
    try:
        if not os.path.exists(TEMPLATE_PATH):
            raise FileNotFoundError(f"Шаблон не найден: {TEMPLATE_PATH}")
        if not os.path.exists(FONT_PATH):
            raise FileNotFoundError(f"Шрифт не найден: {FONT_PATH}")

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        image = Image.open(TEMPLATE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(image)

        try:
            font_bold = ImageFont.truetype(FONT_PATH, 40)
            font = ImageFont.truetype(FONT_PATH, 32)
        except IOError:
            raise FileNotFoundError(f"Ошибка загрузки шрифта: {FONT_PATH}")

        positions = {
            "day": (20, 140),
            "month": (230, 45),
            "year": (385, 140),
            "sum1": (340, 385),
            "sum2": (60, 380),
            "center": (205, 200)
        }

        for key, position in positions.items():
            if key == "center":
                draw.text(position, str(results[key]), font=font_bold, fill="white", anchor="mm")
            else:
                draw.text(position, str(results[key]), font=font, fill="white", anchor="mm")

        image.save(OUTPUT_PATH)
        logger.info(f"Изображение сохранено: {OUTPUT_PATH}")
        return OUTPUT_PATH
    except Exception as e:
        logger.error(f"Ошибка при генерации изображения: {e}")
        return None
