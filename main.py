import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole, Chat
from data_base import start_message
from keyboards import main_menu, get_submenu, menus, start_keyboard


# === Конфигурация ===
BOT_TOKEN = "7657081669:AAGj_PB37i0XdNxPxIrGPSEq43CPAtEUUto"
# Auth token
GIGACHAT_TOKEN = "ODVlZjU1NmUtZTJhNi00YTEwLTg3MGEtMWJlYjdjMWVhZDRiOmU1ZTE4YmZiLTI2MzYtNDkzNC04ZDk4LWE4OGYxODY0ZWQ0NQ=="

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# === Глобальный контекст с системным промптом ===

with open('db.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    print(data)

system_prompt = Messages(
    role=MessagesRole.SYSTEM,
    content=data,
)

# Словарь для хранения диалогов по пользователям (контекст отдельно на каждого)
user_sessions = {}

# Стартовый хендлер

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    # Создаём новый чат с системным промптом
    user_sessions[user_id] = Chat(messages=[system_prompt])

    await message.answer(start_message, reply_markup=main_menu())


async def write_to_file(text: str):
    # Открываем файл в режиме добавления и записываем строку с переводом строки
    with open('db.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + text )

# Хендлер на мероприятие
@dp.message(lambda message: message.text.lower().startswith('мероприя'))
async def handle_meropriyatie(message):
    await write_to_file('\n Добавь этот текст в данные ко всем сотрудникам в поле мероприятие если в поле есть другое мероприятие   вот текст мероприятия:    ' + message.text)
    await message.answer('мероприятие добавлено')

# Хендлер на событие
@dp.message(lambda message: message.text.lower().startswith('событи'))
async def handle_sobyitie(message):
    await write_to_file('\n Добавь этот текст в данные ко всем сотрудникам в поле мероприятие если в поле есть другое мероприятие   вот текст мероприятия:    ' + message.text)
    await message.answer('событие добавлено')

# Хендер для общения с ИИ
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text

    # Инициализация чата, если пользователь пишет впервые
    if user_id not in user_sessions:
        user_sessions[user_id] = Chat(messages=[system_prompt])

    payload = user_sessions[user_id]

    # Если бот перестанет работать значит кончились токены нужно изменить model='GigaChat-2-Max' на 'GigaChat-2-Pro'
    try:
        with GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False, model='GigaChat-2-Max') as giga: #model='GigaChat-2-Pro' #
            # Добавляем сообщение пользователя
            payload.messages.append(Messages(role=MessagesRole.USER, content=user_input))

            # Получаем ответ от GigaChat
            response = giga.chat(payload)

            # Сохраняем ответ в контексте
            reply_msg = response.choices[0].message
            payload.messages.append(reply_msg)

            # Отправляем ответ пользователю
            await message.answer(reply_msg.content)

    except Exception as e:
        await message.answer("Произошла ошибка.")
        print("Unexpected error:", e)

# Обработка нажатий
@dp.callback_query()
async def handle_callback(callback):
    data = callback.data

    responses = {
        "search_name": "🔍 Введите имя сотрудника для поиска:",
        "search_dept": "🏢 Введите название отдела для поиска::",
        "search_proj": "📁 Введите название проекта для поиска::",
        "events_calendar": "📅 Введите 'Покажи ближайшие мероприятия'",
        "birthdays": "🎂 Введите 'Покажи ближайшие дни рождения'",
        "propose_event": "✏️ Введите 'Мероприятие' и Текст предложенного вами мероприятия",
        "my_tasks": "📆 Введите 'Покажи ближайшие задачи'",
        "reminders": "⏰ Введите 'покажи имеющиеся напоминания'",
        "colleagues_busy": "🗓️ Введите 'занятость ивана'",
        "view_calendar": "📥 Введите 'какой календарь на сегодня'",
        "add_event": "📤 Введите 'Событие' и Текст предложенного вами События",
        "find_lunch": "🍽️ Введите 'кто сейчас обедает'",
        "find_game": "🎮 Введите 'кто сейчас свободен для игры'",
        "edit_profile": "🧩 Напишите что бы вы хотели изменить в профиле",
    }

    if data == "main_menu":
        await callback.message.edit_text("🔙 Главное меню", reply_markup=main_menu())

    elif data in menus:
        await callback.message.edit_text("📂 Выберите действие:", reply_markup=get_submenu(data))

    elif data in responses:
        await callback.message.answer(responses[data], reply_markup=main_menu())
        await callback.answer()  # Убираем "часики"

    elif data == "menu_ai":
        await callback.message.answer("✍️ Напиши свой вопрос, я подключаюсь к AI и всё найду.")
        await callback.answer()
    # else:
    #     await callback.answer("⏳ Функция в разработке.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
