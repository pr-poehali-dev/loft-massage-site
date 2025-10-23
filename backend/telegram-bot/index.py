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

def get_available_slots(selected_date: str) -> list:
    """Get available time slots for a given date"""
    all_slots = [
        "10:00", "11:00", "12:00", "13:00", "14:00", 
        "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"
    ]
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT booking_time FROM t_p16986787_loft_massage_site.bookings "
                "WHERE booking_date = %s AND status = 'active'",
                (selected_date,)
            )
            booked_slots = [row['booking_time'] for row in cur.fetchall()]
            return [slot for slot in all_slots if slot not in booked_slots]
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
                "SET status = 'cancelled' WHERE id = %s",
                (booking_id,)
            )
            conn.commit()
            return True
    finally:
        conn.close()

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
        user_data = {}
        
        if text == '/start':
            keyboard = {
                'keyboard': [
                    [{'text': '📅 Записаться на массаж'}],
                    [{'text': '📋 Мои записи'}]
                ],
                'resize_keyboard': True
            }
            send_telegram_message(
                chat_id,
                "👋 Добро пожаловать в Loft Massage!\n\n"
                "Выберите действие:",
                keyboard
            )
        
        elif text == '📅 Записаться на массаж':
            keyboard = {
                'keyboard': [
                    [{'text': 'Классический массаж'}],
                    [{'text': 'Спортивный массаж'}],
                    [{'text': 'Расслабляющий массаж'}],
                    [{'text': '↩️ Назад'}]
                ],
                'resize_keyboard': True
            }
            send_telegram_message(
                chat_id,
                "Выберите тип массажа:",
                keyboard
            )
        
        elif text in ['Классический массаж', 'Спортивный массаж', 'Расслабляющий массаж']:
            user_data['service'] = text
            today = datetime.now()
            dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            
            keyboard = {
                'keyboard': [[{'text': date}] for date in dates] + [[{'text': '↩️ Назад'}]],
                'resize_keyboard': True
            }
            send_telegram_message(
                chat_id,
                f"Вы выбрали: {text}\n\nВыберите дату:",
                keyboard
            )
        
        elif text == '📋 Мои записи':
            send_telegram_message(
                chat_id,
                "Отправьте ваш номер телефона в формате +7XXXXXXXXXX"
            )
        
        elif text == '↩️ Назад':
            keyboard = {
                'keyboard': [
                    [{'text': '📅 Записаться на массаж'}],
                    [{'text': '📋 Мои записи'}]
                ],
                'resize_keyboard': True
            }
            send_telegram_message(chat_id, "Главное меню:", keyboard)
        
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