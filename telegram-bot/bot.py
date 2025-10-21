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
    waiting_for_service = State()
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

# Виды массажа
MASSAGE_SERVICES = {
    "classic_back": {
        "name": "Классический массаж спина",
        "duration": 30,
        "price": "1600₽",
        "description": "Позволит вам почувствовать легкость в теле и избавит от скованности в движениях"
    },
    "relaxing_back": {
        "name": "Успокаивающий массаж спина",
        "duration": 30,
        "price": "1600₽",
        "description": "Мягкие движения помогут расслабиться, снять стресс и восстановить гармонию"
    },
    "classic_body": {
        "name": "Классический массаж тело",
        "duration": 60,
        "price": "2600₽",
        "description": "Комплексная проработка всего тела, улучшает кровообращение"
    },
    "relaxing_body": {
        "name": "Расслабляющий массаж тела",
        "duration": 60,
        "price": "2600₽",
        "description": "Позволяет собраться с мыслями, отпустить тревоги и заботы"
    }
}

# Длительность сеанса в минутах (по умолчанию)
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

def is_slot_available(date_str: str, time_str: str, duration: int) -> bool:
    """Проверить, свободен ли слот с учетом длительности услуги"""
    booking_key = f"{date_str}_{time_str}"
    return booking_key not in bookings

def get_available_times(date_str: str, service_duration: int = 60):
    """Получить доступные слоты времени на выбранную дату с учетом длительности услуги"""
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
            if is_slot_available(date_str, time_str, service_duration):
                available_slots.append(time_str)
            current_time += timedelta(minutes=service_duration)
        
        # Вечерние слоты (17:00-20:00)
        current_time = datetime.strptime(evening_start, "%H:%M")
        end_time = datetime.strptime(evening_end, "%H:%M")
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            if is_slot_available(date_str, time_str, service_duration):
                available_slots.append(time_str)
            current_time += timedelta(minutes=service_duration)
    
    # Для Сб, Вс: один длинный рабочий день (9:00-20:00)
    else:
        work_start, work_end = schedule[0], schedule[1]
        current_time = datetime.strptime(work_start, "%H:%M")
        end_time = datetime.strptime(work_end, "%H:%M")
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            if is_slot_available(date_str, time_str, service_duration):
                available_slots.append(time_str)
            current_time += timedelta(minutes=service_duration)
    
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
    await state.set_state(BookingStates.waiting_for_service)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"💆‍♂️ {MASSAGE_SERVICES['classic_back']['name']} - {MASSAGE_SERVICES['classic_back']['price']} (30 мин)",
            callback_data="service_classic_back"
        )],
        [InlineKeyboardButton(
            text=f"✨ {MASSAGE_SERVICES['relaxing_back']['name']} - {MASSAGE_SERVICES['relaxing_back']['price']} (30 мин)",
            callback_data="service_relaxing_back"
        )],
        [InlineKeyboardButton(
            text=f"🧘 {MASSAGE_SERVICES['classic_body']['name']} - {MASSAGE_SERVICES['classic_body']['price']} (60 мин)",
            callback_data="service_classic_body"
        )],
        [InlineKeyboardButton(
            text=f"💫 {MASSAGE_SERVICES['relaxing_body']['name']} - {MASSAGE_SERVICES['relaxing_body']['price']} (60 мин)",
            callback_data="service_relaxing_body"
        )]
    ])
    
    await message.answer(
        "📝 Начнем запись!\n\n"
        "Выберите вид массажа:",
        reply_markup=keyboard
    )

# Обработка выбора услуги
@dp.callback_query(F.data.startswith("service_"))
async def process_service_selection(callback: F.CallbackQuery, state: FSMContext):
    service_key = callback.data.replace("service_", "")
    service = MASSAGE_SERVICES[service_key]
    
    await state.update_data(
        service_key=service_key,
        service_name=service['name'],
        service_price=service['price'],
        service_duration=service['duration']
    )
    
    await state.set_state(BookingStates.waiting_for_name)
    
    await callback.message.answer(
        f"Вы выбрали: {service['name']}\n"
        f"💰 Цена: {service['price']}\n"
        f"⏱ Длительность: {service['duration']} минут\n\n"
        "Как вас зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.answer()

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
    
    # Получаем длительность выбранной услуги
    data = await state.get_data()
    service_duration = data.get('service_duration', 60)
    
    # Получаем доступные слоты с учетом длительности
    available_times = get_available_times(date_str, service_duration)
    
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
    
    # Получаем длительность услуги для проверки
    service_duration = data.get('service_duration', 60)
    
    # Проверяем, что выбранное время доступно
    available_times = get_available_times(date_str, service_duration)
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
        "service_name": data.get('service_name', 'Массаж'),
        "service_price": data.get('service_price', ''),
        "service_duration": service_duration,
        "user_id": message.from_user.id,
        "username": message.from_user.username
    }
    save_bookings()
    
    # Формируем сообщение для пользователя
    confirmation = (
        "✅ Ваша запись успешно создана!\n\n"
        f"💆‍♂️ Услуга: {data.get('service_name', 'Массаж')}\n"
        f"💰 Цена: {data.get('service_price', '')}\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📅 Дата: {date_str}\n"
        f"🕐 Время: {time_str}\n"
        f"⏱ Длительность: {service_duration} минут\n\n"
        "📍 Жду вас! Скоро свяжусь для подтверждения.\n\n"
        "Для отмены записи используйте /myBookings"
    )
    
    # Отправляем подтверждение клиенту
    await message.answer(confirmation, reply_markup=ReplyKeyboardRemove())
    
    # Отправляем уведомление администратору
    admin_message = (
        "🔔 Новая запись на массаж!\n\n"
        f"💆‍♂️ Услуга: {data.get('service_name', 'Массаж')}\n"
        f"💰 Цена: {data.get('service_price', '')}\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📅 Дата: {date_str}\n"
        f"🕐 Время: {time_str}\n"
        f"⏱ Длительность: {service_duration} мин\n"
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
        service_name = booking.get('service_name', 'Массаж')
        service_price = booking.get('service_price', '')
        duration = booking.get('service_duration', 60)
        message_text += (
            f"💆‍♂️ {service_name}\n"
            f"💰 {service_price}\n"
            f"📅 {booking['date']} в {booking['time']}\n"
            f"⏱ {duration} минут\n\n"
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