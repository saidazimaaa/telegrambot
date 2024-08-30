from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Ваши данные для подключения к API
api_id = 22957426
api_hash = "4af013cf971d55d07a351c04b72a1a2c"
bot_token = "7416310164:AAGXfL7cW9xSYd42uddzcG2jtjA-tqSt6Kw"

# Создаем клиент
app = Client("FBMSurgeryBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Словарь для хранения данных пользователей
users_data = {}

@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    if user_id not in users_data:
        message.reply_text(
            "Добро пожаловать! Этот бот создан для помощи студентам хирургической секции ФФМ МГУ. "
            "Пожалуйста, введите ваше имя и фамилию для регистрации:"
        )
    else:
        show_main_menu(client, message)

@app.on_message(filters.text & ~filters.command(["start"]))
def register(client, message):
    user_id = message.from_user.id
    if user_id not in users_data:
        # Сохраняем имя и фамилию
        users_data[user_id] = {"name": message.text}
        # Здесь можно добавить код для записи данных в Google Sheets
        message.reply_text(f"Спасибо за регистрацию, {users_data[user_id]['name']}!")
        show_main_menu(client, message)
    else:
        message.reply_text("Вы уже зарегистрированы!")

def show_main_menu(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Библиотека книг", callback_data="library")],
        [InlineKeyboardButton("📅 Контроль посещаемости", callback_data="attendance")],
        [InlineKeyboardButton("📰 Новости", callback_data="news")],
        [InlineKeyboardButton("👥 Сообщество", callback_data="community")]
    ])
    message.reply_text("Выберите раздел:", reply_markup=keyboard)

@app.on_callback_query()
def callback_query(client, callback_query):
    if callback_query.data == "library":
        show_library_menu(client, callback_query.message)
    elif callback_query.data in ["abdominal_surgery", "basic_books", "lectures", "neurosurgery", "perelman",
                                 "plastic_surgery", "cardiac_surgery", "thoracic_surgery", "traumatology",
                                 "urology", "endoscopic_surgery"]:
        show_subsection_menu(client, callback_query.message, callback_query.data)
    elif callback_query.data == "attendance":
        show_attendance_menu(client, callback_query.message)
    elif callback_query.data == "news":
        show_news_menu(client, callback_query.message)
    elif callback_query.data == "community":
        show_community_menu(client, callback_query.message)
    elif callback_query.data == "back_to_library":
        show_library_menu(client, callback_query.message)
    elif callback_query.data == "back_to_main_menu":
        show_main_menu(client, callback_query.message)

def show_library_menu(client, message):
    library_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Абдоминальная хирургия", callback_data="abdominal_surgery")],
        [InlineKeyboardButton("Базовые учебники", callback_data="basic_books")],
        [InlineKeyboardButton("Лекции", callback_data="lectures")],
        [InlineKeyboardButton("Нейрохирургия", callback_data="neurosurgery")],
        [InlineKeyboardButton("Перельман", callback_data="perelman")],
        [InlineKeyboardButton("Пластическая хирургия", callback_data="plastic_surgery")],
        [InlineKeyboardButton("Сердечно-сосудистая хирургия", callback_data="cardiac_surgery")],
        [InlineKeyboardButton("Торакальная хирургия", callback_data="thoracic_surgery")],
        [InlineKeyboardButton("Травматология", callback_data="traumatology")],
        [InlineKeyboardButton("Урология", callback_data="urology")],
        [InlineKeyboardButton("Эндовидеохирургия", callback_data="endoscopic_surgery")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main_menu")]
    ])
    message.edit_text("Выберите раздел библиотеки книг:", reply_markup=library_keyboard)

def show_subsection_menu(client, message, section_name):
    subsection_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_library")],
        [InlineKeyboardButton("🏠 Общее меню", callback_data="back_to_main_menu")]
    ])
    
    # Названия разделов на русском языке
    section_titles = {
        "abdominal_surgery": "Абдоминальная хирургия",
        "basic_books": "Базовые учебники",
        "lectures": "Лекции",
        "neurosurgery": "Нейрохирургия",
        "perelman": "Перельман",
        "plastic_surgery": "Пластическая хирургия",
        "cardiac_surgery": "Сердечно-сосудистая хирургия",
        "thoracic_surgery": "Торакальная хирургия",
        "traumatology": "Травматология",
        "urology": "Урология",
        "endoscopic_surgery": "Эндовидеохирургия"
    }
    
    selected_section = section_titles.get(section_name, "Неизвестный раздел")
    message.edit_text(f"Вы выбрали раздел: {selected_section}", reply_markup=subsection_keyboard)

def show_attendance_menu(client, message):
    attendance_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main_menu")],
        [InlineKeyboardButton("🏠 Общее меню", callback_data="back_to_main_menu")]
    ])
    message.edit_text("Здесь будет контроль посещаемости.", reply_markup=attendance_keyboard)

def show_news_menu(client, message):
    news_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main_menu")],
        [InlineKeyboardButton("🏠 Общее меню", callback_data="back_to_main_menu")]
    ])
    message.edit_text("Здесь будут отображаться новости.", reply_markup=news_keyboard)

def show_community_menu(client, message):
    community_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main_menu")],
        [InlineKeyboardButton("🏠 Общее меню", callback_data="back_to_main_menu")]
    ])
    message.edit_text("Здесь будет информация о сообществе.", reply_markup=community_keyboard)

# Запускаем бота
app.run()
