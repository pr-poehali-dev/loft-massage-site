-- Создание таблицы для записей на массаж
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    booking_date DATE NOT NULL,
    booking_time VARCHAR(10) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    cancel_token VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для быстрого поиска по дате
CREATE INDEX IF NOT EXISTS idx_bookings_date ON bookings(booking_date);

-- Создание индекса для поиска по токену отмены
CREATE INDEX IF NOT EXISTS idx_bookings_cancel_token ON bookings(cancel_token);