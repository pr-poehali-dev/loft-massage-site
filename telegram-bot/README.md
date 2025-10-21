# 🤖 Телеграм-бот для записи на массаж

Бот на Aiogram для автоматизации записи клиентов на сеансы массажа.

## Возможности

- ✅ Сбор данных клиента (имя, телефон, дата, время)
- ✅ Отправка контакта через кнопку
- ✅ Выбор времени из готовых вариантов
- ✅ Уведомления администратору о новых записях
- ✅ Отмена записи командой /cancel

## Установка

### 1. Создайте бота в Telegram

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Укажите название и username бота
4. Скопируйте токен бота

### 2. Узнайте свой Telegram ID

1. Найдите [@userinfobot](https://t.me/userinfobot)
2. Отправьте любое сообщение
3. Скопируйте ваш ID

### 3. Установите зависимости

```bash
cd telegram-bot
pip install -r requirements.txt
```

### 4. Настройте переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните данные:
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_CHAT_ID=123456789
```

### 5. Запустите бота

```bash
python bot.py
```

## Использование

### Команды бота:

- `/start` - Приветствие
- `/book` - Начать запись на массаж
- `/cancel` - Отменить текущую запись

### Процесс записи:

1. Клиент отправляет `/book`
2. Вводит имя
3. Делится номером телефона (кнопка или текст)
4. Указывает дату в формате ДД.ММ.ГГГГ
5. Выбирает время из предложенных вариантов
6. Получает подтверждение

Администратор сразу получает уведомление с данными клиента.

## Настройка времени записи

В функции `get_time_keyboard()` можно изменить доступные часы:

```python
keyboard=[
    [KeyboardButton(text="10:00"), KeyboardButton(text="12:00")],
    [KeyboardButton(text="14:00"), KeyboardButton(text="16:00")],
    [KeyboardButton(text="18:00"), KeyboardButton(text="20:00")]
]
```

## Развертывание на сервере

### Вариант 1: Screen (простой)

```bash
screen -S massage_bot
python bot.py
# Нажмите Ctrl+A, затем D для выхода
```

### Вариант 2: Systemd (рекомендуется)

Создайте файл `/etc/systemd/system/massage-bot.service`:

```ini
[Unit]
Description=Massage Booking Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram-bot
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Запустите сервис:
```bash
sudo systemctl enable massage-bot
sudo systemctl start massage-bot
sudo systemctl status massage-bot
```

## Требования

- Python 3.8+
- aiogram 3.15.0
- python-dotenv 1.0.0
