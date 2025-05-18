from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



# Главное меню кнопка
def start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/start"))
    return keyboard

# Главное меню инлайн
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧑‍💼 Сотрудники", callback_data="menu_employees"),
            InlineKeyboardButton(text="🎉 Мероприятия", callback_data="menu_events"),
            InlineKeyboardButton(text="🕒 Задачи", callback_data="menu_tasks")
        ],
        [
            InlineKeyboardButton(text="📅 Календарь", callback_data="menu_calendar"),
            InlineKeyboardButton(text="🧠 Спросить AI", callback_data="menu_ai"),
            InlineKeyboardButton(text="⚙️ Ещё", callback_data="menu_more")
        ]
    ])
    return kb


# Вложенные инлайн меню
menus = {
    "menu_employees": [
        ("🔍 Поиск по имени", "search_name"),
        ("🏢 Поиск по отделу", "search_dept"),
        ("📁 Поиск по проекту", "search_proj"),
    ],
    "menu_events": [
        ("📅 Календарь событий", "events_calendar"),
        ("🎂 Ближайшие дни рождения", "birthdays"),
        ("✏️ Предложить мероприятие", "propose_event"),
    ],
    "menu_tasks": [
        ("📆 Мой календарь задач", "my_tasks"),
        ("⏰ Напоминания", "reminders"),
        ("🗓️ Занятость коллег", "colleagues_busy"),
    ],
    "menu_calendar": [
        ("📥 Посмотреть мой календарь", "view_calendar"),
        ("📤 Добавить встречу", "add_event"),
    ],
    "menu_more": [
        ("🍽️ Найти коллегу для обеда", "find_lunch"),
        ("🎮 Найти напарника для игры", "find_game"),
        ("🧩 Настроить профиль", "edit_profile"),
    ]
}

# Функция для получения инлайн саб меню

def get_submenu(menu_key):
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=cb)]
        for text, cb in menus[menu_key]
    ]
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
