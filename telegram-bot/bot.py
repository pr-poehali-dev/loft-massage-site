import os
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import json

# Состояния для записи
class BookingStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_date = State()
    waiting_for_time = State()

# Состояния для админ-панели
class AdminStates(StatesGroup):
    waiting_for_day_off_date = State()
    waiting_for_custom_schedule_date = State()
    waiting_for_custom_schedule_time = State()

# Инициализация бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# График работы (день недели: [начало, конец, перерыв_начало, перерыв_конец])
WORK_SCHEDULE = {
    0: ["11:00", "14:00", "17:00", "20:00"],  # Понедельник (утро 11-14, вечер 17-20)
    1: None,  # Вторник - выходной
    2: ["11:00", "14:00", "17:00", "20:00"],  # Среда (утро 11-14, вечер 17-20)
    3: None,  # Четверг - выходной
    4: ["11:00", "14:00", "17:00", "20:00"],  # Пятница (утро 11-14, вечер 17-20)
    5: ["09:00", "20:00", None, None],         # Суббота (без перерыва, 9-20)
    6: ["09:00", "20:00", None, None]  # Воскресенье (без перерыва, 9-20)
}

# Длительность сеанса в минутах
SESSION_DURATION = 60

# Хранилище записей (в продакшене использовать БД)
bookings = {}

# Дополнительные выходные дни (формат: "ДД.ММ.ГГГГ")
extra_days_off = set()

# Кастомное расписание для конкретных дат (формат: {"ДД.ММ.ГГГГ": [начало, конец, ...]})
custom_schedule = {}

def load_bookings():
    """Загрузка записей из файла"""
    global bookings
    try:
        with open('bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except FileNotFoundError:
        bookings = {}

def load_schedule_settings():
    """Загрузка настроек расписания"""
    global extra_days_off, custom_schedule
    try:
        with open('schedule_settings.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            extra_days_off = set(data.get('extra_days_off', []))
            custom_schedule = data.get('custom_schedule', {})
    except FileNotFoundError:
        extra_days_off = set()
        custom_schedule = {}

def save_schedule_settings():
    """Сохранение настроек расписания"""
    with open('schedule_settings.json', 'w', encoding='utf-8') as f:
        json.dump({
            'extra_days_off': list(extra_days_off),
            'custom_schedule': custom_schedule
        }, f, ensure_ascii=False, indent=2)

def save_bookings():
    """Сохранение записей в файл"""
    with open('bookings.json', 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

def get_available_times(date_str: str):
    """Получить доступные слоты времени на выбранную дату"""
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return []
    
    # Проверяем, не выходной ли день (дополнительный)
    if date_str in extra_days_off:
        return []
    
    # Проверяем кастомное расписание для конкретной даты
    if date_str in custom_schedule:
        schedule = custom_schedule[date_str]
        if schedule is None:
            return []
    else:
        weekday = date_obj.weekday()
        # Проверяем, работает ли массажист в этот день
        if WORK_SCHEDULE[weekday] is None:
            return []
        schedule = WORK_SCHEDULE[weekday]
    
    available_slots = []
    weekday = date_obj.weekday()
    
    # Для Пн, Ср, Пт: два рабочих окна (утро и вечер)
    if weekday in [0, 2, 4]:
        morning_start, morning_end, evening_start, evening_end = schedule
        
        # Утренние слоты (11:00-14:00)
        current_time = datetime.strptime(morning_start, "%H:%M")
        end_time = datetime.strptime(morning_end, "%H:%M")
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            booking_key = f"{date_str}_{time_str}"
            if booking_key not in bookings:
                available_slots.append(time_str)
            current_time += timedelta(minutes=SESSION_DURATION)
        
        # Вечерние слоты (17:00-20:00)
        current_time = datetime.strptime(evening_start, "%H:%M")
        end_time = datetime.strptime(evening_end, "%H:%M")
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            booking_key = f"{date_str}_{time_str}"
            if booking_key not in bookings:
                available_slots.append(time_str)
            current_time += timedelta(minutes=SESSION_DURATION)
    
    # Для Сб, Вс: один длинный рабочий день (9:00-20:00)
    else:
        work_start, work_end = schedule[0], schedule[1]
        current_time = datetime.strptime(work_start, "%H:%M")
        end_time = datetime.strptime(work_end, "%H:%M")
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            booking_key = f"{date_str}_{time_str}"
            if booking_key not in bookings:
                available_slots.append(time_str)
            current_time += timedelta(minutes=SESSION_DURATION)
    
    return available_slots

def is_date_available(date_str: str):
    """Проверить, работает ли массажист в эту дату"""
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        
        # Проверяем, что дата не в прошлом
        if date_obj.date() < datetime.now().date():
            return False
        
        weekday = date_obj.weekday()
        return WORK_SCHEDULE[weekday] is not None
    except ValueError:
        return False

def get_time_keyboard(available_times):
    """Создать клавиатуру с доступными слотами"""
    if not available_times:
        return ReplyKeyboardRemove()
    
    # Разбиваем слоты по 3 в ряд
    keyboard = []
    row = []
    for time in available_times:
        row.append(KeyboardButton(text=time))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для записи на массаж.\n\n"
        "📋 График работы:\n"
        "Пн, Ср, Пт: 11:00-14:00 и 17:00-20:00\n"
        "Сб, Вс: 09:00-20:00\n"
        "Вт, Чт: Выходные\n\n"
        "⏱ Длительность сеанса: 60 минут\n\n"
        "Используйте команду /book для записи.",
        reply_markup=ReplyKeyboardRemove()
    )

# Команда /book - начало записи
@dp.message(Command("book"))
async def cmd_book(message: Message, state: FSMContext):
    await state.set_state(BookingStates.waiting_for_name)
    await message.answer(
        "📝 Начнем запись!\n\n"
        "Как вас зовут?",
        reply_markup=ReplyKeyboardRemove()
    )

# Получение имени
@dp.message(BookingStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.waiting_for_phone)
    
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True
    )
    
    await message.answer(
        f"Приятно познакомиться, {message.text}!\n\n"
        "Поделитесь своим номером телефона:",
        reply_markup=phone_keyboard
    )

# Получение телефона
@dp.message(BookingStates.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(BookingStates.waiting_for_date)
    await message.answer(
        "📅 Отлично! Теперь укажите желаемую дату записи.\n\n"
        "📋 График работы:\n"
        "Пн, Ср, Пт: 11:00-14:00 и 17:00-20:00\n"
        "Сб, Вс: 09:00-20:00\n"
        "Вт, Чт: Выходные\n\n"
        "Формат: ДД.ММ.ГГГГ (например, 25.10.2025)",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(BookingStates.waiting_for_phone)
async def process_phone_text(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(BookingStates.waiting_for_date)
    await message.answer(
        "📅 Отлично! Теперь укажите желаемую дату записи.\n\n"
        "📋 График работы:\n"
        "Пн, Ср, Пт: 11:00-14:00 и 17:00-20:00\n"
        "Сб, Вс: 09:00-20:00\n"
        "Вт, Чт: Выходные\n\n"
        "Формат: ДД.ММ.ГГГГ (например, 25.10.2025)",
        reply_markup=ReplyKeyboardRemove()
    )

# Получение даты
@dp.message(BookingStates.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
    date_str = message.text.strip()
    
    # Проверяем формат даты
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ\n"
            "Например: 25.10.2025"
        )
        return
    
    # Проверяем, что дата не в прошлом
    if date_obj.date() < datetime.now().date():
        await message.answer("❌ Нельзя записаться на прошедшую дату. Выберите другую дату.")
        return
    
    # Проверяем, работает ли массажист в этот день
    weekday = date_obj.weekday()
    if WORK_SCHEDULE[weekday] is None:
        day_name = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"][weekday]
        await message.answer(
            f"❌ К сожалению, во {day_name} не работаю (выходной).\n"
            "Пожалуйста, выберите другой день.\n\n"
            "📋 Рабочие дни:\n"
            "Пн, Ср, Пт: 11:00-14:00 и 17:00-20:00\n"
            "Сб, Вс: 09:00-20:00"
        )
        return
    
    # Получаем доступные слоты
    available_times = get_available_times(date_str)
    
    if not available_times:
        await message.answer(
            f"❌ К сожалению, на {date_str} все слоты заняты.\n"
            "Попробуйте выбрать другую дату."
        )
        return
    
    await state.update_data(date=date_str)
    await state.set_state(BookingStates.waiting_for_time)
    
    day_name = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"][weekday]
    
    await message.answer(
        f"📅 {day_name}, {date_str}\n\n"
        f"🕐 Доступные слоты ({len(available_times)}):\n"
        "Выберите удобное время:",
        reply_markup=get_time_keyboard(available_times)
    )

# Получение времени и завершение записи
@dp.message(BookingStates.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    time_str = message.text.strip()
    data = await state.get_data()
    date_str = data['date']
    
    # Проверяем, что выбранное время доступно
    available_times = get_available_times(date_str)
    if time_str not in available_times:
        await message.answer(
            "❌ Это время уже занято или недоступно.\n"
            "Выберите другое время из предложенных."
        )
        return
    
    await state.update_data(time=time_str)
    
    # Сохраняем запись
    booking_key = f"{date_str}_{time_str}"
    bookings[booking_key] = {
        "name": data['name'],
        "phone": data['phone'],
        "date": date_str,
        "time": time_str,
        "user_id": message.from_user.id,
        "username": message.from_user.username
    }
    save_bookings()
    
    # Формируем сообщение для пользователя
    confirmation = (
        "✅ Ваша запись успешно создана!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📅 Дата: {date_str}\n"
        f"🕐 Время: {time_str}\n"
        f"⏱ Длительность: 60 минут\n\n"
        "📍 Жду вас! Скоро свяжусь для подтверждения.\n\n"
        "Для отмены записи используйте /myBookings"
    )
    
    # Отправляем подтверждение клиенту
    await message.answer(confirmation, reply_markup=ReplyKeyboardRemove())
    
    # Отправляем уведомление администратору
    admin_message = (
        "🔔 Новая запись на массаж!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📅 Дата: {date_str}\n"
        f"🕐 Время: {time_str}\n"
        f"👨‍💼 Telegram: @{message.from_user.username or 'Не указан'}\n"
        f"🆔 ID: {message.from_user.id}"
    )
    
    if ADMIN_CHAT_ID:
        await bot.send_message(ADMIN_CHAT_ID, admin_message)
    
    # Очищаем состояние
    await state.clear()

# Команда для просмотра своих записей
@dp.message(Command("myBookings"))
async def cmd_my_bookings(message: Message):
    user_id = message.from_user.id
    user_bookings = []
    
    for key, booking in bookings.items():
        if booking['user_id'] == user_id:
            # Проверяем, что запись не в прошлом
            booking_datetime = datetime.strptime(f"{booking['date']} {booking['time']}", "%d.%m.%Y %H:%M")
            if booking_datetime >= datetime.now():
                user_bookings.append((key, booking))
    
    if not user_bookings:
        await message.answer("У вас нет активных записей.")
        return
    
    # Формируем сообщение со списком записей
    message_text = "📋 Ваши записи:\n\n"
    
    for key, booking in user_bookings:
        message_text += (
            f"📅 {booking['date']} в {booking['time']}\n"
            f"👤 {booking['name']}\n\n"
        )
    
    # Создаем кнопки для отмены
    keyboard = []
    for key, booking in user_bookings:
        keyboard.append([InlineKeyboardButton(
            text=f"❌ Отменить {booking['date']} {booking['time']}",
            callback_data=f"cancel_{key}"
        )])
    
    await message.answer(
        message_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

# Обработка отмены записи
@dp.callback_query(F.data.startswith("cancel_"))
async def process_cancel(callback: F.CallbackQuery):
    booking_key = callback.data.replace("cancel_", "")
    
    if booking_key in bookings:
        booking = bookings[booking_key]
        
        # Проверяем, что это запись текущего пользователя
        if booking['user_id'] == callback.from_user.id:
            del bookings[booking_key]
            save_bookings()
            
            await callback.message.answer(
                f"✅ Запись на {booking['date']} в {booking['time']} отменена."
            )
            
            # Уведомляем админа
            if ADMIN_CHAT_ID:
                await bot.send_message(
                    ADMIN_CHAT_ID,
                    f"❌ Запись отменена клиентом:\n"
                    f"📅 {booking['date']} {booking['time']}\n"
                    f"👤 {booking['name']}\n"
                    f"📱 {booking['phone']}"
                )
        else:
            await callback.answer("Это не ваша запись!", show_alert=True)
    else:
        await callback.answer("Запись уже отменена.", show_alert=True)
    
    await callback.answer()

# Команда /cancel - отмена текущей записи
@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ Процесс записи отменен.\n"
        "Используйте /book для новой записи.",
        reply_markup=ReplyKeyboardRemove()
    )

# ========== АДМИН-ПАНЕЛЬ ==========

def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return str(user_id) == str(ADMIN_CHAT_ID)

@dp.message(Command("admin"))
async def cmd_admin(message: Message):
    """Админ-панель управления расписанием"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к админ-панели.")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Добавить выходной день", callback_data="admin_add_dayoff")],
        [InlineKeyboardButton(text="🗓 Посмотреть выходные", callback_data="admin_view_dayoffs")],
        [InlineKeyboardButton(text="🔄 Изменить график на день", callback_data="admin_custom_schedule")],
        [InlineKeyboardButton(text="📊 Все записи", callback_data="admin_all_bookings")],
        [InlineKeyboardButton(text="🗑 Очистить старые записи", callback_data="admin_clear_old")]
    ])
    
    await message.answer(
        "⚙️ Админ-панель управления расписанием\n\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

# Просмотр всех записей (админ)
@dp.callback_query(F.data == "admin_all_bookings")
async def admin_all_bookings(callback: F.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    if not bookings:
        await callback.message.answer("📋 Записей пока нет.")
        await callback.answer()
        return
    
    # Группируем записи по датам
    bookings_by_date = {}
    for key, booking in bookings.items():
        date = booking['date']
        if date not in bookings_by_date:
            bookings_by_date[date] = []
        bookings_by_date[date].append(booking)
    
    # Сортируем даты
    sorted_dates = sorted(bookings_by_date.keys(), key=lambda x: datetime.strptime(x, "%d.%m.%Y"))
    
    message_text = "📊 Все записи:\n\n"
    for date in sorted_dates:
        message_text += f"📅 {date}:\n"
        for booking in sorted(bookings_by_date[date], key=lambda x: x['time']):
            message_text += f"  • {booking['time']} - {booking['name']} ({booking['phone']})\n"
        message_text += "\n"
    
    await callback.message.answer(message_text)
    await callback.answer()

# Добавление выходного дня
@dp.callback_query(F.data == "admin_add_dayoff")
async def admin_add_dayoff(callback: F.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_for_day_off_date)
    await callback.message.answer(
        "📅 Введите дату дополнительного выходного дня\n"
        "Формат: ДД.ММ.ГГГГ (например, 01.01.2026)"
    )
    await callback.answer()

@dp.message(AdminStates.waiting_for_day_off_date)
async def process_day_off_date(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    date_str = message.text.strip()
    
    # Проверяем формат даты
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        await message.answer("❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ")
        return
    
    extra_days_off.add(date_str)
    save_schedule_settings()
    
    await message.answer(f"✅ Выходной день {date_str} добавлен!")
    await state.clear()

# Просмотр выходных дней
@dp.callback_query(F.data == "admin_view_dayoffs")
async def admin_view_dayoffs(callback: F.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    if not extra_days_off:
        await callback.message.answer("📅 Дополнительных выходных нет.")
        await callback.answer()
        return
    
    sorted_days = sorted(extra_days_off, key=lambda x: datetime.strptime(x, "%d.%m.%Y"))
    
    message_text = "📅 Дополнительные выходные дни:\n\n"
    keyboard = []
    
    for day in sorted_days:
        message_text += f"• {day}\n"
        keyboard.append([InlineKeyboardButton(
            text=f"❌ Удалить {day}",
            callback_data=f"remove_dayoff_{day}"
        )])
    
    await callback.message.answer(
        message_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
    await callback.answer()

# Удаление выходного дня
@dp.callback_query(F.data.startswith("remove_dayoff_"))
async def remove_dayoff(callback: F.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    date_str = callback.data.replace("remove_dayoff_", "")
    
    if date_str in extra_days_off:
        extra_days_off.remove(date_str)
        save_schedule_settings()
        await callback.message.answer(f"✅ Выходной день {date_str} удален!")
    
    await callback.answer()

# Изменение графика на конкретный день
@dp.callback_query(F.data == "admin_custom_schedule")
async def admin_custom_schedule(callback: F.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_for_custom_schedule_date)
    await callback.message.answer(
        "🗓 Введите дату для изменения графика\n"
        "Формат: ДД.ММ.ГГГГ (например, 25.12.2025)"
    )
    await callback.answer()

@dp.message(AdminStates.waiting_for_custom_schedule_date)
async def process_custom_schedule_date(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    date_str = message.text.strip()
    
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        await message.answer("❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ")
        return
    
    await state.update_data(custom_date=date_str)
    await state.set_state(AdminStates.waiting_for_custom_schedule_time)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сделать выходным", callback_data="custom_dayoff")],
        [InlineKeyboardButton(text="09:00-20:00 (весь день)", callback_data="custom_full")],
        [InlineKeyboardButton(text="11:00-14:00 и 17:00-20:00", callback_data="custom_split")],
        [InlineKeyboardButton(text="Отмена", callback_data="custom_cancel")]
    ])
    
    await message.answer(
        f"📅 Настройка графика на {date_str}\n\n"
        "Выберите вариант работы:",
        reply_markup=keyboard
    )

@dp.callback_query(F.data.startswith("custom_"))
async def process_custom_schedule_type(callback: F.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    data = await state.get_data()
    date_str = data.get('custom_date')
    
    action = callback.data.replace("custom_", "")
    
    if action == "cancel":
        await state.clear()
        await callback.message.answer("❌ Отменено")
        await callback.answer()
        return
    
    if action == "dayoff":
        custom_schedule[date_str] = None
    elif action == "full":
        custom_schedule[date_str] = ["09:00", "20:00", None, None]
    elif action == "split":
        custom_schedule[date_str] = ["11:00", "14:00", "17:00", "20:00"]
    
    save_schedule_settings()
    
    await callback.message.answer(f"✅ График на {date_str} изменен!")
    await state.clear()
    await callback.answer()

# Очистка старых записей
@dp.callback_query(F.data == "admin_clear_old")
async def admin_clear_old(callback: F.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    today = datetime.now().date()
    old_bookings = []
    
    for key, booking in list(bookings.items()):
        booking_date = datetime.strptime(booking['date'], "%d.%m.%Y").date()
        if booking_date < today:
            old_bookings.append(key)
            del bookings[key]
    
    if old_bookings:
        save_bookings()
        await callback.message.answer(f"✅ Удалено {len(old_bookings)} старых записей")
    else:
        await callback.message.answer("📋 Старых записей нет")
    
    await callback.answer()

# Запуск бота
async def main():
    load_bookings()
    load_schedule_settings()
    print("🤖 Бот запущен!")
    print(f"📋 Загружено записей: {len(bookings)}")
    print(f"📅 Дополнительных выходных: {len(extra_days_off)}")
    print(f"🗓 Кастомных расписаний: {len(custom_schedule)}")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())