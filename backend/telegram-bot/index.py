"""
Business: Telegram bot webhook handler for massage booking service
Args: event with httpMethod, body from Telegram; context with request_id
Returns: HTTP response for Telegram webhook
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor

user_states = {}

def send_telegram_message(chat_id: str, text: str, reply_markup: Optional[Dict] = None) -> None:
    """Send message via Telegram Bot API"""
    import urllib.request
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        return
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    if reply_markup:
        payload['reply_markup'] = reply_markup
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass

def get_db_connection():
    """Get database connection using DATABASE_URL"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError('DATABASE_URL not set')
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

def get_available_times(date_str: str) -> list:
    """Get available time slots for a given date based on schedule"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    day_of_week = date_obj.weekday()
    
    if day_of_week in [1, 3]:
        return []
    
    if day_of_week in [5, 6]:
        times = [f"{h}:00" for h in range(9, 20)]
    else:
        times = [f"{h}:00" for h in range(11, 14)] + [f"{h}:00" for h in range(17, 20)]
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT booking_time FROM t_p16986787_loft_massage_site.bookings "
                "WHERE booking_date = %s AND status = 'active'",
                (date_str,)
            )
            booked = [row['booking_time'] for row in cur.fetchall()]
            return [t for t in times if t not in booked]
    finally:
        conn.close()

def create_booking(service: str, date: str, time: str, name: str, phone: str) -> int:
    """Create new booking in database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO t_p16986787_loft_massage_site.bookings "
                "(service, booking_date, booking_time, customer_name, customer_phone, status) "
                "VALUES (%s, %s, %s, %s, %s, 'active') RETURNING id",
                (service, date, time, name, phone)
            )
            booking_id = cur.fetchone()['id']
            conn.commit()
            
            notify_admin(booking_id, service, date, time, name, phone)
            return booking_id
    finally:
        conn.close()

def get_user_bookings(phone: str) -> list:
    """Get user's active bookings"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, service, booking_date, booking_time "
                "FROM t_p16986787_loft_massage_site.bookings "
                "WHERE customer_phone = %s AND status = 'active' "
                "ORDER BY booking_date, booking_time",
                (phone,)
            )
            return cur.fetchall()
    finally:
        conn.close()

def cancel_booking(booking_id: int) -> bool:
    """Cancel booking by ID"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE t_p16986787_loft_massage_site.bookings "
                "SET status = 'cancelled' WHERE id = %s AND status = 'active'",
                (booking_id,)
            )
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()

def get_all_active_bookings() -> list:
    """Get all active bookings (for admin)"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, service, booking_date, booking_time, customer_name, customer_phone "
                "FROM t_p16986787_loft_massage_site.bookings "
                "WHERE status = 'active' "
                "ORDER BY booking_date, booking_time"
            )
            return cur.fetchall()
    finally:
        conn.close()

def is_admin(chat_id: str) -> bool:
    """Check if user is admin"""
    admin_chat_id = os.environ.get('ADMIN_CHAT_ID')
    return admin_chat_id and str(chat_id) == str(admin_chat_id)

def notify_admin(booking_id: int, service: str, date: str, time: str, name: str, phone: str) -> None:
    """Send notification to admin about new booking"""
    admin_chat_id = os.environ.get('ADMIN_CHAT_ID')
    if not admin_chat_id:
        return
    
    message = (
        f"🆕 <b>Новая запись!</b>\n\n"
        f"📋 ID: {booking_id}\n"
        f"💆 Услуга: {service}\n"
        f"📅 Дата: {date}\n"
        f"🕐 Время: {time}\n"
        f"👤 Клиент: {name}\n"
        f"📞 Телефон: {phone}"
    )
    
    send_telegram_message(admin_chat_id, message)

def get_day_name(date_str: str) -> str:
    """Get day name in Russian"""
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return days[date_obj.weekday()]

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Telegram bot webhook handler
    """
    method = event.get('httpMethod', 'POST')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'isBase64Encoded': False,
            'body': ''
        }
    
    if method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'isBase64Encoded': False,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        update = json.loads(event.get('body', '{}'))
        
        if 'message' not in update:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'isBase64Encoded': False,
                'body': json.dumps({'ok': True})
            }
        
        message = update['message']
        chat_id = str(message['chat']['id'])
        text = message.get('text', '')
        
        if chat_id not in user_states:
            user_states[chat_id] = {}
        
        state = user_states[chat_id]
        
        if text == '/start' or text == '↩️ Назад':
            user_states[chat_id] = {}
            
            if is_admin(chat_id):
                keyboard = {
                    'keyboard': [
                        [{'text': '📅 Записаться на массаж'}],
                        [{'text': '📋 Мои записи'}],
                        [{'text': '⚙️ Все записи (админ)'}, {'text': '❌ Отменить запись'}]
                    ],
                    'resize_keyboard': True
                }
            else:
                keyboard = {
                    'keyboard': [
                        [{'text': '📅 Записаться на массаж'}],
                        [{'text': '📋 Мои записи'}]
                    ],
                    'resize_keyboard': True
                }
            
            send_telegram_message(
                chat_id,
                "👋 Добро пожаловать в Loft Massage!\n\nВыберите действие:",
                keyboard
            )
        
        elif text == '📅 Записаться на массаж':
            user_states[chat_id] = {'step': 'choose_service'}
            keyboard = {
                'keyboard': [
                    [{'text': 'Классический массаж спина'}],
                    [{'text': 'Успокаивающий массаж спина'}],
                    [{'text': 'Классический массаж тело'}],
                    [{'text': 'Расслабляющий массаж тела'}],
                    [{'text': '↩️ Назад'}]
                ],
                'resize_keyboard': True
            }
            send_telegram_message(chat_id, "Выберите тип массажа:", keyboard)
        
        elif state.get('step') == 'choose_service' and text in [
            'Классический массаж спина', 
            'Успокаивающий массаж спина', 
            'Классический массаж тело', 
            'Расслабляющий массаж тела'
        ]:
            user_states[chat_id]['service'] = text
            user_states[chat_id]['step'] = 'choose_date'
            
            today = datetime.now()
            dates = []
            keyboard_rows = []
            
            for i in range(14):
                check_date = today + timedelta(days=i)
                date_str = check_date.strftime('%Y-%m-%d')
                day_name = get_day_name(date_str)
                
                if check_date.weekday() not in [1, 3]:
                    display = f"{day_name} {check_date.strftime('%d.%m')}"
                    dates.append(date_str)
                    keyboard_rows.append([{'text': display, 'callback_data': date_str}])
            
            keyboard = {
                'keyboard': keyboard_rows[:7] + [[{'text': '↩️ Назад'}]],
                'resize_keyboard': True
            }
            send_telegram_message(chat_id, f"Вы выбрали: {text}\n\nВыберите дату:", keyboard)
        
        elif state.get('step') == 'choose_date':
            try:
                parts = text.split()
                if len(parts) >= 2:
                    date_part = parts[1]
                    day, month = date_part.split('.')
                    year = datetime.now().year
                    date_obj = datetime(year, int(month), int(day))
                    date_str = date_obj.strftime('%Y-%m-%d')
                    
                    user_states[chat_id]['date'] = date_str
                    user_states[chat_id]['step'] = 'choose_time'
                    
                    available_times = get_available_times(date_str)
                    
                    if not available_times:
                        send_telegram_message(chat_id, "К сожалению, на эту дату нет свободных мест. Выберите другую дату.")
                    else:
                        keyboard = {
                            'keyboard': [[{'text': t}] for t in available_times] + [[{'text': '↩️ Назад'}]],
                            'resize_keyboard': True
                        }
                        send_telegram_message(chat_id, "Выберите время:", keyboard)
            except:
                send_telegram_message(chat_id, "Пожалуйста, выберите дату из предложенных вариантов")
        
        elif state.get('step') == 'choose_time' and ':' in text:
            user_states[chat_id]['time'] = text
            user_states[chat_id]['step'] = 'enter_name'
            
            keyboard = {'remove_keyboard': True}
            send_telegram_message(chat_id, "Введите ваше имя:", keyboard)
        
        elif state.get('step') == 'enter_name':
            user_states[chat_id]['name'] = text
            user_states[chat_id]['step'] = 'enter_phone'
            send_telegram_message(chat_id, "Введите ваш номер телефона (например: +79001234567):")
        
        elif state.get('step') == 'enter_phone':
            user_states[chat_id]['phone'] = text
            
            service = state['service']
            date = state['date']
            time = state['time']
            name = state['name']
            phone = text
            
            booking_id = create_booking(service, date, time, name, phone)
            
            keyboard = {
                'keyboard': [
                    [{'text': '📅 Записаться на массаж'}],
                    [{'text': '📋 Мои записи'}]
                ],
                'resize_keyboard': True
            }
            
            send_telegram_message(
                chat_id,
                f"✅ <b>Запись создана!</b>\n\n"
                f"📋 ID: {booking_id}\n"
                f"💆 Услуга: {service}\n"
                f"📅 Дата: {date}\n"
                f"🕐 Время: {time}\n"
                f"👤 Имя: {name}\n"
                f"📞 Телефон: {phone}",
                keyboard
            )
            
            user_states[chat_id] = {}
        
        elif text == '📋 Мои записи':
            user_states[chat_id] = {'step': 'my_bookings'}
            keyboard = {'remove_keyboard': True}
            send_telegram_message(chat_id, "Отправьте ваш номер телефона:", keyboard)
        
        elif state.get('step') == 'my_bookings':
            bookings = get_user_bookings(text)
            
            if not bookings:
                keyboard = {
                    'keyboard': [
                        [{'text': '📅 Записаться на массаж'}],
                        [{'text': '↩️ Назад'}]
                    ],
                    'resize_keyboard': True
                }
                send_telegram_message(chat_id, "У вас нет активных записей", keyboard)
            else:
                msg = "📋 <b>Ваши записи:</b>\n\n"
                for b in bookings:
                    msg += f"ID: {b['id']}\n"
                    msg += f"💆 {b['service']}\n"
                    msg += f"📅 {b['booking_date']}\n"
                    msg += f"🕐 {b['booking_time']}\n\n"
                
                keyboard = {
                    'keyboard': [
                        [{'text': '📅 Записаться на массаж'}],
                        [{'text': '↩️ Назад'}]
                    ],
                    'resize_keyboard': True
                }
                send_telegram_message(chat_id, msg, keyboard)
            
            user_states[chat_id] = {}
        
        elif text == '⚙️ Все записи (админ)' and is_admin(chat_id):
            bookings = get_all_active_bookings()
            
            if not bookings:
                send_telegram_message(chat_id, "📋 Нет активных записей")
            else:
                msg = "📋 <b>Все активные записи:</b>\n\n"
                for b in bookings:
                    msg += f"🆔 ID: <b>{b['id']}</b>\n"
                    msg += f"💆 {b['service']}\n"
                    msg += f"📅 {b['booking_date']}\n"
                    msg += f"🕐 {b['booking_time']}\n"
                    msg += f"👤 {b['customer_name']}\n"
                    msg += f"📞 {b['customer_phone']}\n\n"
                
                send_telegram_message(chat_id, msg)
        
        elif text == '❌ Отменить запись' and is_admin(chat_id):
            user_states[chat_id] = {'step': 'admin_cancel'}
            keyboard = {'remove_keyboard': True}
            send_telegram_message(chat_id, "Введите ID записи для отмены:", keyboard)
        
        elif state.get('step') == 'admin_cancel' and is_admin(chat_id):
            try:
                booking_id = int(text)
                if cancel_booking(booking_id):
                    keyboard = {
                        'keyboard': [
                            [{'text': '📅 Записаться на массаж'}],
                            [{'text': '📋 Мои записи'}],
                            [{'text': '⚙️ Все записи (админ)'}, {'text': '❌ Отменить запись'}]
                        ],
                        'resize_keyboard': True
                    }
                    send_telegram_message(chat_id, f"✅ Запись #{booking_id} успешно отменена", keyboard)
                else:
                    send_telegram_message(chat_id, f"❌ Запись #{booking_id} не найдена или уже отменена")
            except ValueError:
                send_telegram_message(chat_id, "❌ Пожалуйста, введите корректный ID (число)")
            
            user_states[chat_id] = {}
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'isBase64Encoded': False,
            'body': json.dumps({'ok': True})
        }
        
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'isBase64Encoded': False,
            'body': json.dumps({'ok': True})
        }