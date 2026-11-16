from urllib.parse import quote

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


MANAGER_USERNAME = "pristanol"

MANAGER_MESSAGE = (
    "Привет! Я готов оформить банковский продукт. "
    "Заполнил анкету в боте. Подскажи, пожалуйста, дальнейшие шаги."
)


def get_yes_no_inline():
    """Кнопки Да/Нет"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="yes"),
                InlineKeyboardButton(text="Нет", callback_data="no"),
            ]
        ]
    )


def get_banks_inline():
    """Кнопки выбора банков"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏦 Альфа Банк", callback_data="bank_alfa")],
            [InlineKeyboardButton(text="🏦 Т Банк", callback_data="bank_t")],
            [InlineKeyboardButton(text="🏦 Сбербанк", callback_data="bank_sber")],
            [InlineKeyboardButton(text="🏦 ВТБ Банк", callback_data="bank_vtb")],
            [InlineKeyboardButton(text="🏦 ПСБ", callback_data="bank_psb")],
            [InlineKeyboardButton(text="🏦 Озон банк", callback_data="bank_ozon")],
            [InlineKeyboardButton(text="🏦 УралСиб", callback_data="bank_uralsib")],
            [InlineKeyboardButton(text="🏦 Точка Банк", callback_data="bank_tochka")],
            [InlineKeyboardButton(text="✅ Всё, закончил выбор", callback_data="banks_done")],
        ]
    )


def get_manager_inline():
    """Кнопка перехода к менеджеру с готовым текстом"""
    url = (
        f"https://t.me/{MANAGER_USERNAME}"
        f"?text={quote(MANAGER_MESSAGE)}"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написать менеджеру",
                    url=url
                )
            ]
        ]
    )
