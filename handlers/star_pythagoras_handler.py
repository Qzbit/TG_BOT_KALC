from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup
import os
from calculators.star_pythagoras import calculate_star_pythagoras, generate_star_image
import logging

def handle_star_pythagoras(birth_date):
    day, month, year = map(int, birth_date.split("."))
    results = calculate_star_pythagoras(day, month, year)
    return generate_star_image(results)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Пути к файлам
TEMPLATE_PATH = "templates/star_pythagoras_template.png"
FONT_PATH = "fonts/arial.ttf"
RESULT_IMAGE = "generated_images/star_result.png"

# Уменьшение числа до одной цифры
def reduce_to_single_digit(num):
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

# Расчёт чисел звезды Пифагора
def calculate_star_pythagoras(day, month, year):
    day_num = reduce_to_single_digit(day)
    month_num = reduce_to_single_digit(month)
    year_num = reduce_to_single_digit(sum(map(int, str(year))))
    sum1 = reduce_to_single_digit(day_num + month_num + year_num)
    sum2 = reduce_to_single_digit(day_num + month_num + year_num + sum1)
    center = reduce_to_single_digit(day_num + month_num + year_num + sum1 + sum2)

    logger.info(f"Результаты расчета: day={day_num}, month={month_num}, year={year_num}, sum1={sum1}, sum2={sum2}, center={center}")

    return {
        "day": day_num,
        "month": month_num,
        "year": year_num,
        "sum1": sum1,
        "sum2": sum2,
        "center": center,
    }

# Генерация изображения
def generate_star_image(results):
    try:
        # Проверка файлов
        if not os.path.exists(TEMPLATE_PATH):
            raise FileNotFoundError(f"Файл шаблона не найден: {TEMPLATE_PATH}")
        if not os.path.exists(FONT_PATH):
            raise FileNotFoundError(f"Шрифт не найден: {FONT_PATH}")

        # Убедиться, что директория для результата существует
        os.makedirs(os.path.dirname(RESULT_IMAGE), exist_ok=True)

        # Открытие шаблона
        base_image = Image.open(TEMPLATE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(base_image)
        font = ImageFont.truetype(FONT_PATH, 30)

        # Координаты для текста
        positions = {
            "day": (20, 140),     # Верхняя точка
            "month": (230, 45),   # Правая верхняя точка
            "year": (385, 140),   # Правая нижняя точка
            "sum1": (340, 385),   # Левая нижняя точка
            "sum2": (60, 380),    # Левая верхняя точка
            "center": (205, 200)  # Центр
        }

        # Рисуем текст
        for key, position in positions.items():
            draw.text(position, str(results[key]), font=font, fill="white", anchor="mm")

        # Сохранение результата
        base_image.save(RESULT_IMAGE)
        logger.info(f"Изображение сохранено: {RESULT_IMAGE}")
        return RESULT_IMAGE

    except Exception as e:
        logger.error(f"Ошибка при генерации изображения: {e}")
        raise RuntimeError(f"Ошибка при генерации изображения: {e}")

# Регистрация обработчиков
def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "Звезда Пифагора")
    def ask_birthdate(message):
        """Запрашивает дату рождения у пользователя."""
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(
            message.chat.id,
            "Введите вашу дату рождения в формате ДД.ММ.ГГГГ, например, 17.07.1988:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(message, handle_birthdate)

    def handle_birthdate(message):
        """Обрабатывает введённую дату рождения, рассчитывает и отправляет изображение."""
        try:
            # Проверка формата даты
            birthdate = datetime.strptime(message.text.strip(), "%d.%m.%Y")
            results = calculate_star_pythagoras(birthdate.day, birthdate.month, birthdate.year)

            # Генерация изображения
            image_path = generate_star_image(results)

            # Отправка изображения
            with open(image_path, "rb") as image:
                bot.send_photo(message.chat.id, image)

        except ValueError:
            logger.warning("Некорректный формат даты")
            bot.send_message(message.chat.id, "Ошибка: Некорректная дата. Попробуйте снова.")
        except FileNotFoundError as fnfe:
            logger.error(f"Ошибка файла: {fnfe}")
            bot.send_message(message.chat.id, f"Ошибка: {fnfe}. Убедитесь, что все файлы на месте.")
        except Exception as e:
            logger.error(f"Общая ошибка: {e}")
            bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
