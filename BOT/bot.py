import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from keyboards import (
    get_yes_no_inline,
    get_banks_inline,
    get_manager_inline,
)
from offers import (
    get_all_offers,
    get_available_offers,
    format_offers_list,
)


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("9221454963:AAGUj5sPjlDEhyxJo50cyWJwDiFZaJx1gtM")

OWNER_IDS = [8321550731, 5334318285]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    waiting_for_earnings = State()
    waiting_for_age = State()
    waiting_for_ip = State()
    waiting_for_banks = State()
    waiting_for_city = State()


BANKS_MAP = {
    "bank_alfa": "Альфа Банк",
    "bank_t": "Т Банк",
    "bank_sber": "Сбербанк",
    "bank_vtb": "ВТБ Банк",
    "bank_psb": "ПСБ",
    "bank_ozon": "Озон банк",
    "bank_uralsib": "УралСиб",
    "bank_tochka": "Точка Банк",
}


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Привет! Готов ли ты рассмотреть возможность получить "
        "от 2 000₽ до 6 500₽ за оформление банковского продукта "
        "при выполнении условий программы?",
        reply_markup=get_yes_no_inline()
    )

    await state.set_state(Form.waiting_for_earnings)


@dp.callback_query(
    Form.waiting_for_earnings,
    F.data.in_(["yes", "no"])
)
async def process_earnings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    answer = "Да" if callback.data == "yes" else "Нет"
    await state.update_data(earnings_ready=answer)

    await callback.message.edit_text(
        "Сколько тебе лет? (введи число)"
    )

    await state.set_state(Form.waiting_for_age)


@dp.message(Form.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text.strip())

        if age < 18:
            await message.answer(
                "К сожалению, сервис доступен только с 18 лет."
            )
            await state.clear()
            return

        if age > 120:
            await message.answer("Пожалуйста, введи корректный возраст.")
            return

        await state.update_data(age=age)

        await message.answer(
            "Есть ли у тебя открытое ИП?",
            reply_markup=get_yes_no_inline()
        )

        await state.set_state(Form.waiting_for_ip)

    except (ValueError, AttributeError):
        await message.answer("Пожалуйста, введи возраст числом.")


@dp.callback_query(
    Form.waiting_for_ip,
    F.data.in_(["yes", "no"])
)
async def process_ip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    answer = "Да" if callback.data == "yes" else "Нет"
    await state.update_data(has_ip=answer)

    if answer == "Да":
        await state.update_data(selected_banks=[])

        await callback.message.edit_text(
            "🏦 В каких банках у тебя есть расчётные счета?\n\n"
            "Выбери все подходящие варианты и нажми "
            "«✅ Всё, закончил выбор».",
            reply_markup=get_banks_inline()
        )

        await state.set_state(Form.waiting_for_banks)

    else:
        await state.update_data(selected_banks="Нет ИП")

        await callback.message.edit_text(
            "📍 Из какого ты города? (введи название)"
        )

        await state.set_state(Form.waiting_for_city)


@dp.callback_query(Form.waiting_for_banks)
async def process_banks(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    selected_banks = data.get("selected_banks", [])

    if callback.data == "banks_done":
        if not selected_banks:
            await callback.message.edit_text(
                "⚠️ Пожалуйста, выбери хотя бы один банк.",
                reply_markup=get_banks_inline()
            )
            return

        await state.update_data(selected_banks=selected_banks)

        await callback.message.edit_text(
            "📍 Из какого ты города? (введи название)"
        )

        await state.set_state(Form.waiting_for_city)
        return

    if callback.data in BANKS_MAP:
        bank_name = BANKS_MAP[callback.data]

        if bank_name not in selected_banks:
            selected_banks.append(bank_name)
            await state.update_data(selected_banks=selected_banks)

            banks_list = ", ".join(selected_banks)

            await callback.message.edit_text(
                f"✅ Добавил: {bank_name}\n\n"
                f"📋 Выбранные банки: {banks_list}\n\n"
                "Выбери ещё банки или нажми "
                "«✅ Всё, закончил выбор».",
                reply_markup=get_banks_inline()
            )
        else:
            await callback.message.edit_text(
                f"⚠️ «{bank_name}» уже выбран.\n\n"
                f"📋 Выбранные банки: {', '.join(selected_banks)}\n\n"
                "Выбери другой банк или заверши выбор.",
                reply_markup=get_banks_inline()
            )


@dp.message(Form.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введи название города.")
        return

    city = message.text.strip()

    if not city:
        await message.answer("Пожалуйста, введи название города.")
        return

    await state.update_data(city=city)
    data = await state.get_data()

    selected_banks = data["selected_banks"]

    if selected_banks == "Нет ИП":
        available_offers = get_all_offers()
        banks_text = "Нет ИП"
    else:
        available_offers = get_available_offers(selected_banks)
        banks_text = ", ".join(selected_banks)

    offers_text = format_offers_list(available_offers)
    offers_count = len(available_offers)

    username = message.from_user.username or "Не указан"
    user_id = message.from_user.id
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    application_text = (
        "🔔 НОВАЯ ЗАЯВКА\n\n"
        f"👤 Пользователь: @{username}\n"
        f"🆔 ID: {user_id}\n"
        f"🕐 Время: {timestamp}\n\n"
        "📋 Ответы:\n"
        f"• Готов рассмотреть предложения: {data['earnings_ready']}\n"
        f"• Возраст: {data['age']}\n"
        f"• Есть ИП: {data['has_ip']}\n"
        f"• Банки с РКО: {banks_text}\n"
        f"• Город: {city}\n\n"
        f"{offers_text}"
    )

    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(
                chat_id=owner_id,
                text=application_text
            )
        except Exception:
            logging.exception(
                "Не удалось отправить заявку владельцу %s",
                owner_id
            )

    await message.answer(
        "✅ Анкета заполнена!\n\n"
        f"📊 Доступно предложений: {offers_count}\n\n"
        "Если хочешь обсудить оформление и уточнить условия, "
        "нажми кнопку ниже. Откроется личный чат с менеджером, "
        "где будет подготовлено сообщение.",
        reply_markup=get_manager_inline()
    )

    await state.clear()


async def main():
    await dp.start_polling(bot)


if name == "main":
    asyncio.run(main())
