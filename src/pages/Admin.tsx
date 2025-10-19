import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import Icon from '@/components/ui/icon'

interface Booking {
  id: number
  service: string
  booking_date: string
  booking_time: string
  customer_name: string
  customer_phone: string
  status: string
  cancel_token: string
  created_at: string
}

export default function Admin() {
  const [bookings, setBookings] = useState<Booking[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().split('T')[0])
  const [filter, setFilter] = useState<'all' | 'active' | 'cancelled'>('active')

  const loadBookings = async () => {
    setLoading(true)
    try {
      const response = await fetch('https://functions.poehali.dev/44725468-4f39-4361-bc48-b76fb53f5e04')
      const data = await response.json()
      setBookings(data)
    } catch (error) {
      console.error('Ошибка загрузки записей:', error)
    }
    setLoading(false)
  }

  useEffect(() => {
    loadBookings()
  }, [])

  const cancelBooking = async (id: number) => {
    if (!confirm('Отменить эту запись?')) return
    
    try {
      const response = await fetch(`https://functions.poehali.dev/44725468-4f39-4361-bc48-b76fb53f5e04?id=${id}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        alert('Запись отменена')
        loadBookings()
      }
    } catch (error) {
      alert('Ошибка при отмене записи')
    }
  }

  const filteredBookings = bookings
    .filter(b => filter === 'all' ? true : b.status === filter)
    .filter(b => selectedDate ? b.booking_date === selectedDate : true)
    .sort((a, b) => {
      if (a.booking_date === b.booking_date) {
        return a.booking_time.localeCompare(b.booking_time)
      }
      return a.booking_date.localeCompare(b.booking_date)
    })

  const stats = {
    total: bookings.length,
    active: bookings.filter(b => b.status === 'active').length,
    cancelled: bookings.filter(b => b.status === 'cancelled').length
  }

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Админ-панель</h1>
          <p className="text-foreground/70">Управление записями на массаж</p>
        </div>

        {/* Статистика */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-foreground/70">Всего записей</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">{stats.total}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-foreground/70">Активные</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-green-600">{stats.active}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-foreground/70">Отменённые</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-red-600">{stats.cancelled}</p>
            </CardContent>
          </Card>
        </div>

        {/* Фильтры */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <label className="block text-sm font-medium mb-2">Дата</label>
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className="w-full p-3 rounded-lg border-2 border-border focus:border-industrial outline-none"
                />
              </div>
              <div className="flex-1">
                <label className="block text-sm font-medium mb-2">Статус</label>
                <select
                  value={filter}
                  onChange={(e) => setFilter(e.target.value as any)}
                  className="w-full p-3 rounded-lg border-2 border-border focus:border-industrial outline-none"
                >
                  <option value="all">Все записи</option>
                  <option value="active">Активные</option>
                  <option value="cancelled">Отменённые</option>
                </select>
              </div>
              <div className="flex items-end">
                <Button onClick={loadBookings} className="bg-industrial hover:bg-industrial/90 text-white">
                  <Icon name="RefreshCw" size={20} className="mr-2" />
                  Обновить
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Список записей */}
        <Card>
          <CardHeader>
            <CardTitle>Записи ({filteredBookings.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">
                <p className="text-foreground/70">Загрузка...</p>
              </div>
            ) : filteredBookings.length === 0 ? (
              <div className="text-center py-8">
                <Icon name="Calendar" size={48} className="mx-auto text-foreground/20 mb-4" />
                <p className="text-foreground/70">Нет записей</p>
              </div>
            ) : (
              <div className="space-y-4">
                {filteredBookings.map(booking => (
                  <div
                    key={booking.id}
                    className={`border-2 rounded-lg p-4 ${
                      booking.status === 'cancelled' 
                        ? 'border-red-200 bg-red-50/50' 
                        : 'border-border hover:border-industrial/50'
                    }`}
                  >
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-start gap-3 mb-2">
                          <Icon 
                            name={booking.status === 'cancelled' ? 'XCircle' : 'CheckCircle'} 
                            className={booking.status === 'cancelled' ? 'text-red-600' : 'text-green-600'} 
                            size={20} 
                          />
                          <div>
                            <h3 className="font-semibold text-lg">{booking.service}</h3>
                            <p className="text-foreground/70">
                              {new Date(booking.booking_date).toLocaleDateString('ru-RU', { 
                                day: 'numeric', 
                                month: 'long',
                                year: 'numeric'
                              })} в {booking.booking_time}
                            </p>
                          </div>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3 text-sm">
                          <div className="flex items-center gap-2">
                            <Icon name="User" size={16} className="text-foreground/50" />
                            <span>{booking.customer_name}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Icon name="Phone" size={16} className="text-foreground/50" />
                            <span>{booking.customer_phone}</span>
                          </div>
                        </div>
                      </div>
                      
                      {booking.status === 'active' && (
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              const cancelUrl = `${window.location.origin}/cancel?token=${booking.cancel_token}`
                              navigator.clipboard.writeText(cancelUrl)
                              alert('Ссылка для отмены скопирована в буфер обмена')
                            }}
                          >
                            <Icon name="Link" size={16} className="mr-2" />
                            Ссылка
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => cancelBooking(booking.id)}
                          >
                            <Icon name="Trash2" size={16} className="mr-2" />
                            Отменить
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}