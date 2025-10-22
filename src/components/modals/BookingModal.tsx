import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Icon from '@/components/ui/icon'

interface Service {
  title: string
  description: string
  icon: string
  prices: { duration: string; price: string }[]
}

interface BookingModalProps {
  show: boolean
  onClose: () => void
  services: Service[]
  selectedService: string | null
  setSelectedService: (service: string | null) => void
  selectedDate: Date | null
  setSelectedDate: (date: Date | null) => void
  selectedTime: string | null
  setSelectedTime: (time: string | null) => void
  customerName: string
  setCustomerName: (name: string) => void
  customerPhone: string
  setCustomerPhone: (phone: string) => void
  onConfirmBooking: () => void
}

export default function BookingModal({
  show,
  onClose,
  services,
  selectedService,
  setSelectedService,
  selectedDate,
  setSelectedDate,
  selectedTime,
  setSelectedTime,
  customerName,
  setCustomerName,
  customerPhone,
  setCustomerPhone,
  onConfirmBooking
}: BookingModalProps) {
  if (!show) return null

  return (
    <div 
      className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fade-in overflow-y-auto"
      onClick={onClose}
    >
      <Card className="max-w-2xl w-full" onClick={(e) => e.stopPropagation()}>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-2xl">Онлайн запись</CardTitle>
              <CardDescription>Выберите дату, время и услугу</CardDescription>
            </div>
            <button 
              className="text-foreground/70 hover:text-foreground transition-colors"
              onClick={onClose}
            >
              <Icon name="X" size={24} />
            </button>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Выбор услуги */}
          <div>
            <h3 className="font-semibold mb-3">Выберите услугу</h3>
            <div className="grid grid-cols-1 gap-2">
              {services.map((service, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedService(service.title)}
                  className={`p-4 rounded-lg border-2 text-left transition-all ${
                    selectedService === service.title 
                      ? 'border-industrial bg-industrial/10' 
                      : 'border-border hover:border-industrial/50'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold">{service.title}</p>
                      <p className="text-sm text-foreground/70">{service.prices[0].duration}</p>
                    </div>
                    <p className="font-bold text-industrial">{service.prices[0].price}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Выбор даты */}
          <div>
            <h3 className="font-semibold mb-3">Выберите дату</h3>
            <input 
              type="date"
              min={new Date().toISOString().split('T')[0]}
              onChange={(e) => {
                setSelectedDate(new Date(e.target.value))
                setSelectedTime(null)
              }}
              className="w-full p-3 rounded-lg border-2 border-border focus:border-industrial outline-none"
            />
          </div>

          {/* Выбор времени */}
          {selectedDate && (
            <div>
              <h3 className="font-semibold mb-3">Выберите время</h3>
              <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                {(() => {
                  const day = selectedDate.getDay()
                  const isWeekend = day === 0 || day === 6
                  const isWorkDay = day === 1 || day === 3 || day === 5
                  
                  if (!isWeekend && !isWorkDay) {
                    return <p className="text-foreground/70 col-span-full">Выходной день</p>
                  }
                  
                  const times = []
                  if (isWorkDay) {
                    for (let h = 11; h < 14; h++) {
                      times.push(`${h}:00`)
                    }
                    for (let h = 17; h < 20; h++) {
                      times.push(`${h}:00`)
                    }
                  } else {
                    for (let h = 9; h < 20; h++) {
                      times.push(`${h}:00`)
                    }
                  }
                  
                  return times.map(time => (
                    <button
                      key={time}
                      onClick={() => setSelectedTime(time)}
                      className={`p-3 rounded-lg border-2 transition-all ${
                        selectedTime === time 
                          ? 'border-industrial bg-industrial text-white' 
                          : 'border-border hover:border-industrial/50'
                      }`}
                    >
                      {time}
                    </button>
                  ))
                })()}
              </div>
            </div>
          )}

          {/* Контактные данные */}
          {selectedTime && (
            <div className="space-y-4">
              <h3 className="font-semibold">Ваши контакты</h3>
              <input 
                type="text"
                placeholder="Ваше имя"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                className="w-full p-3 rounded-lg border-2 border-border focus:border-industrial outline-none"
              />
              <input 
                type="tel"
                placeholder="Телефон"
                value={customerPhone}
                onChange={(e) => setCustomerPhone(e.target.value)}
                className="w-full p-3 rounded-lg border-2 border-border focus:border-industrial outline-none"
              />
            </div>
          )}

          {/* Кнопка записи */}
          {selectedService && selectedDate && selectedTime && customerName && customerPhone && (
            <Button 
              className="w-full bg-industrial hover:bg-industrial/90 text-white text-lg py-6"
              onClick={onConfirmBooking}
            >
              Подтвердить запись
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  )
}