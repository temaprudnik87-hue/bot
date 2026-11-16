OFFERS = {
    "Альфа Банк": [
        {
            "name": "ИП + РКО Альфа",
            "payout": 16000,
            "client_payout": 4000,
            "condition": "Пополнение на 3000₽",
            "time": "15 минут"
        }
    ],
    "Т Банк": [
        {
            "name": "РКО Т-Банк",
            "payout": 11310,
            "client_payout": 3500,
            "condition": "Поступление 3000₽ от хоздеятельности (холд 30 дней)",
            "time": "20 минут"
        }
    ],
    "Сбербанк": [
        {
            "name": "РКО Сбер",
            "payout": 8000,
            "client_payout": 2500,
            "condition": "Активный оборот от 3000₽",
            "time": "25 минут"
        }
    ],
    "ВТБ Банк": [
        {
            "name": "РКО ВТБ",
            "payout": 10100,
            "client_payout": 3000,
            "condition": "Пополнение + выдержка денег",
            "time": "30 минут"
        }
    ],
    "ПСБ": [
        {
            "name": "РКО ПСБ + Карта",
            "payout": 13666,
            "client_payout": 4000,
            "condition": "РКО + оформление карты",
            "time": "20 минут"
        }
    ],
    "Озон банк": [
        {
            "name": "ИП Озон",
            "payout": 14000,
            "client_payout": 4000,
            "condition": "Активный оборот от 3000₽",
            "time": "15 минут"
        }
    ],
    "Точка Банк": [
        {
            "name": "ИП Точка",
            "payout": 7500,
            "client_payout": 2350,
            "condition": "Платёжное поручение",
            "time": "15 минут"
        }
    ],
    "УралСиб": [
        {
            "name": "ИП УралСиб",
            "payout": 8100,
            "client_payout": 4000,
            "condition": "Подключение тарифа",
            "time": "15 минут"
        }
    ]
}


ADDITIONAL_OFFERS = [
    {
        "name": "Билайн для бизнеса",
        "payout": 6000,
        "client_payout": 2000,
        "condition": "Подключение корпоративной связи",
        "time": "10 минут"
    }
]


def get_all_offers():
    """Возвращает все доступные офферы"""
    available = []

    for offers in OFFERS.values():
        available.extend(offers)

    available.extend(ADDITIONAL_OFFERS)
    return available


def get_available_offers(selected_banks):
    """Исключает офферы банков, в которых у клиента уже есть РКО"""
    if selected_banks == "Нет ИП":
        return get_all_offers()

    available = []

    for bank, offers in OFFERS.items():
        if bank not in selected_banks:
            available.extend(offers)

    available.extend(ADDITIONAL_OFFERS)
    return available


def format_offers_list(offers):
    """Форматирует список офферов"""
    if not offers:
        return "К сожалению, сейчас нет доступных офферов."

    text = "📋 Доступные предложения:\n\n"

    for i, offer in enumerate(offers, 1):
        text += f"{i}. {offer['name']}\n"
        text += f"   💰 Вознаграждение клиенту: {offer['client_payout']}₽\n"
        text += f"   📝 Условие: {offer['condition']}\n"
        text += f"   ⏱️ Время: {offer['time']}\n\n"

    return text
