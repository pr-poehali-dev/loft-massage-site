'''
Business: API для управления записями на массаж (создание, получение, отмена)
Args: event с httpMethod, body, queryStringParameters
Returns: HTTP response с данными записей или статусом операции
'''

import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any
import secrets
from datetime import datetime

def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(database_url)

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    method: str = event.get('httpMethod', 'GET')
    
    # Handle CORS OPTIONS request
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Admin-Token',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # GET - получить все записи или одну по токену
        if method == 'GET':
            params = event.get('queryStringParameters', {}) or {}
            cancel_token = params.get('token')
            date_filter = params.get('date')
            
            if cancel_token:
                cursor.execute(
                    "SELECT * FROM bookings WHERE cancel_token = %s",
                    (cancel_token,)
                )
                booking = cursor.fetchone()
                if not booking:
                    return {
                        'statusCode': 404,
                        'headers': headers,
                        'body': json.dumps({'error': 'Запись не найдена'}),
                        'isBase64Encoded': False
                    }
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(dict(booking), default=str),
                    'isBase64Encoded': False
                }
            
            # Получить все записи (для админ-панели)
            if date_filter:
                cursor.execute(
                    "SELECT * FROM bookings WHERE booking_date = %s ORDER BY booking_time",
                    (date_filter,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM bookings WHERE status = 'active' ORDER BY booking_date, booking_time"
                )
            
            bookings = cursor.fetchall()
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps([dict(b) for b in bookings], default=str),
                'isBase64Encoded': False
            }
        
        # POST - создать новую запись
        elif method == 'POST':
            body_data = json.loads(event.get('body', '{}'))
            
            service = body_data.get('service')
            booking_date = body_data.get('booking_date')
            booking_time = body_data.get('booking_time')
            customer_name = body_data.get('customer_name')
            customer_phone = body_data.get('customer_phone')
            
            if not all([service, booking_date, booking_time, customer_name, customer_phone]):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Все поля обязательны'}),
                    'isBase64Encoded': False
                }
            
            # Проверка на существующую запись в это время
            cursor.execute(
                "SELECT id FROM bookings WHERE booking_date = %s AND booking_time = %s AND status = 'active'",
                (booking_date, booking_time)
            )
            existing = cursor.fetchone()
            if existing:
                return {
                    'statusCode': 409,
                    'headers': headers,
                    'body': json.dumps({'error': 'Это время уже занято'}),
                    'isBase64Encoded': False
                }
            
            cancel_token = secrets.token_urlsafe(32)
            
            cursor.execute(
                """INSERT INTO bookings 
                (service, booking_date, booking_time, customer_name, customer_phone, cancel_token)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *""",
                (service, booking_date, booking_time, customer_name, customer_phone, cancel_token)
            )
            
            new_booking = cursor.fetchone()
            conn.commit()
            
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps(dict(new_booking), default=str),
                'isBase64Encoded': False
            }
        
        # DELETE - отменить запись (по токену или по ID для админа)
        elif method == 'DELETE':
            params = event.get('queryStringParameters', {}) or {}
            cancel_token = params.get('token')
            booking_id = params.get('id')
            
            if cancel_token:
                cursor.execute(
                    "UPDATE bookings SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE cancel_token = %s RETURNING *",
                    (cancel_token,)
                )
            elif booking_id:
                cursor.execute(
                    "UPDATE bookings SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
                    (booking_id,)
                )
            else:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Требуется token или id'}),
                    'isBase64Encoded': False
                }
            
            cancelled_booking = cursor.fetchone()
            if not cancelled_booking:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'error': 'Запись не найдена'}),
                    'isBase64Encoded': False
                }
            
            conn.commit()
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Запись отменена', 'booking': dict(cancelled_booking)}, default=str),
                'isBase64Encoded': False
            }
        
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'}),
            'isBase64Encoded': False
        }
    
    except Exception as e:
        conn.rollback()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)}),
            'isBase64Encoded': False
        }
    
    finally:
        cursor.close()
        conn.close()
