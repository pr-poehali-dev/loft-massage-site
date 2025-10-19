import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import Icon from '@/components/ui/icon'
import { API_ENDPOINTS } from '@/config/api'

interface Booking {
  id: number
  service: string
  booking_date: string
  booking_time: string
  customer_name: string
  status: string
}

export default function Cancel() {
  const [booking, setBooking] = useState<Booking | null>(null)
  const [loading, setLoading] = useState(true)
  const [cancelled, setCancelled] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const token = params.get('token')

    if (!token) {
      setError('Неверная ссылка для отмены')
      setLoading(false)
      return
    }

    loadBooking(token)
  }, [])

  const loadBooking = async (token: string) => {
    try {
      const response = await fetch(`${API_ENDPOINTS.bookings}?token=${token}`)
      const data = await response.json()

      if (response.ok) {
        if (data.status === 'cancelled') {
          setCancelled(true)
        }
        setBooking(data)
      } else {
        setError('Запись не найдена')
      }
    } catch (error) {
      setError('Ошибка соединения с сервером')
    }
    setLoading(false)
  }

  const cancelBooking = async () => {
    if (!booking) return

    const params = new URLSearchParams(window.location.search)
    const token = params.get('token')

    try {
      const response = await fetch(`${API_ENDPOINTS.bookings}?token=${token}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        setCancelled(true)
        setBooking({ ...booking, status: 'cancelled' })
      } else {
        alert('Не удалось отменить запись')
      }
    } catch (error) {
      alert('Ошибка соединения с сервером')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardContent className="pt-6 text-center">
            <p className="text-foreground/70">Загрузка...</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-600">
              <Icon name="XCircle" size={24} />
              Ошибка
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-foreground/70">{error}</p>
            <Button 
              className="w-full mt-4"
              onClick={() => window.location.href = '/'}
            >
              Вернуться на главную
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (cancelled) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-600">
              <Icon name="CheckCircle" size={24} />
              Запись отменена
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-foreground/70 mb-4">
              Ваша запись успешно отменена. Вы можете записаться на другое время через сайт.
            </p>
            {booking && (
              <div className="bg-muted p-4 rounded-lg mb-4">
                <p className="text-sm font-semibold mb-2">Детали отменённой записи:</p>
                <p className="text-sm text-foreground/70">Услуга: {booking.service}</p>
                <p className="text-sm text-foreground/70">
                  Дата: {new Date(booking.booking_date).toLocaleDateString('ru-RU')} в {booking.booking_time}
                </p>
                <p className="text-sm text-foreground/70">Имя: {booking.customer_name}</p>
              </div>
            )}
            <Button 
              className="w-full bg-industrial hover:bg-industrial/90 text-white"
              onClick={() => window.location.href = '/'}
            >
              Записаться снова
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="max-w-md w-full">
        <CardHeader>
          <CardTitle>Отмена записи</CardTitle>
        </CardHeader>
        <CardContent>
          {booking && (
            <>
              <div className="bg-muted p-4 rounded-lg mb-6">
                <p className="text-sm font-semibold mb-2">Детали записи:</p>
                <p className="text-sm text-foreground/70">Услуга: {booking.service}</p>
                <p className="text-sm text-foreground/70">
                  Дата: {new Date(booking.booking_date).toLocaleDateString('ru-RU')} в {booking.booking_time}
                </p>
                <p className="text-sm text-foreground/70">Имя: {booking.customer_name}</p>
              </div>
              
              <p className="text-foreground/70 mb-6">
                Вы уверены, что хотите отменить эту запись?
              </p>

              <div className="flex gap-3">
                <Button 
                  variant="outline"
                  className="flex-1"
                  onClick={() => window.location.href = '/'}
                >
                  Назад
                </Button>
                <Button 
                  variant="destructive"
                  className="flex-1"
                  onClick={cancelBooking}
                >
                  Отменить запись
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}