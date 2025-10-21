import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

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

# Клавиатура для времени
def get_time_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="10:00"), KeyboardButton(text="12:00")],
            [KeyboardButton(text="14:00"), KeyboardButton(text="16:00")],
            [KeyboardButton(text="18:00"), KeyboardButton(text="20:00")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для записи на массаж.\n\n"
        "Используйте команду /book для записи на сеанс.",
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
        "Отлично! Теперь укажите желаемую дату записи.\n"
        "Формат: ДД.ММ.ГГГГ (например, 25.10.2025)",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(BookingStates.waiting_for_phone)
async def process_phone_text(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(BookingStates.waiting_for_date)
    await message.answer(
        "Отлично! Теперь укажите желаемую дату записи.\n"
        "Формат: ДД.ММ.ГГГГ (например, 25.10.2025)",
        reply_markup=ReplyKeyboardRemove()
    )

# Получение даты
@dp.message(BookingStates.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
    try:
        # Проверяем формат даты
        date_obj = datetime.strptime(message.text, "%d.%m.%Y")
        await state.update_data(date=message.text)
        await state.set_state(BookingStates.waiting_for_time)
        await message.answer(
            "Выберите удобное время:",
            reply_markup=get_time_keyboard()
        )
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ\n"
            "Например: 25.10.2025"
        )

# Получение времени и завершение записи
@dp.message(BookingStates.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    
    # Получаем все данные
    data = await state.get_data()
    
    # Формируем сообщение для пользователя
    confirmation = (
        "✅ Ваша запись принята!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📅 Дата: {data['date']}\n"
        f"🕐 Время: {data['time']}\n\n"
        "Скоро с вами свяжется мастер для подтверждения."
    )
    
    # Отправляем подтверждение клиенту
    await message.answer(confirmation, reply_markup=ReplyKeyboardRemove())
    
    # Отправляем уведомление администратору
    admin_message = (
        "🔔 Новая запись на массаж!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📅 Дата: {data['date']}\n"
        f"🕐 Время: {data['time']}\n"
        f"👨‍💼 Telegram: @{message.from_user.username or 'Не указан'}"
    )
    
    if ADMIN_CHAT_ID:
        await bot.send_message(ADMIN_CHAT_ID, admin_message)
    
    # Очищаем состояние
    await state.clear()

# Команда /cancel - отмена записи
@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ Запись отменена.\n"
        "Используйте /book для новой записи.",
        reply_markup=ReplyKeyboardRemove()
    )

# Запуск бота
async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
