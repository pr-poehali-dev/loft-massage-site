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

def load_bookings():
    """Загрузка записей из файла"""
    global bookings
    try:
        with open('bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except FileNotFoundError:
        bookings = {}

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
    
    weekday = date_obj.weekday()
    
    # Проверяем, работает ли массажист в этот день
    if WORK_SCHEDULE[weekday] is None:
        return []
    
    schedule = WORK_SCHEDULE[weekday]
    available_slots = []
    
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
        "⏱ Длительность сеанса: 30-60 минут\n\n"
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
        await message.answer(
            "❌ К сожалению, в воскресенье не работаю.\n"
            "Пожалуйста, выберите другой день."
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

# Запуск бота
async def main():
    load_bookings()
    print("🤖 Бот запущен!")
    print(f"📋 Загружено записей: {len(bookings)}")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())