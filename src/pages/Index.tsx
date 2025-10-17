import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import Icon from '@/components/ui/icon'

export default function Index() {
  const [bookingUrl] = useState('#')
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [showCertificates, setShowCertificates] = useState(false)
  const [showBooking, setShowBooking] = useState(false)
  const [selectedDate, setSelectedDate] = useState<Date | null>(null)
  const [selectedTime, setSelectedTime] = useState<string | null>(null)
  const [selectedService, setSelectedService] = useState<string | null>(null)
  const [customerName, setCustomerName] = useState('')
  const [customerPhone, setCustomerPhone] = useState('')

  const services = [
    {
      title: 'Классический массаж спина',
      description: 'Этот массаж позволит вам почувствовать легкость в теле и избавит вас от скованности в движениях. Отлично подходит тем кто усердно работает над собой или очень устает на работе. Подарит легкий заряд бодрости и наполняет вас силой',
      icon: 'Hand',
      prices: [
        { duration: '30 минут', price: '1600₽' }
      ]
    },
    {
      title: 'Успокаивающий массаж спина',
      description: 'Этот массаж создан специально для тех, кто нуждается в эмоциональной разгрузке. Мягкие, плавные движения помогут вам расслабиться, снять стресс и восстановить внутреннюю гармонию. Идеален после напряженного дня',
      icon: 'Sparkles',
      prices: [
        { duration: '30 минут', price: '1600₽' }
      ]
    },
    {
      title: 'Классический массаж тело',
      description: 'Комплексная проработка всего тела. Улучшает кровообращение, снимает мышечное напряжение и дарит чувство обновления. Вы почувствуете как каждая клеточка вашего тела наполняется энергией и жизненной силой',
      icon: 'User',
      prices: [
        { duration: '60 минут', price: '2600₽' }
      ]
    },
    {
      title: 'Расслабляющий массаж тела',
      description: 'Массаж позволяющий вам собраться с мыслями, отпустить все ваши тревоги и заботы. Отдохните телом и душой пока руки мастера творят свое волшебство',
      icon: 'Heart',
      prices: [
        { duration: '60 минут', price: '2600₽' }
      ]
    }
  ]

  const gallery = [
    'https://cdn.poehali.dev/files/e1832efa-4a2d-41cb-b464-51b3e1d6974b.jpeg',
    'https://cdn.poehali.dev/files/ca89434b-6670-4b10-9942-f9b1f36a7f7a.jpeg',
    'https://cdn.poehali.dev/files/73991933-3d6d-476a-be3e-da7f0c43bc38.jpeg',
    'https://cdn.poehali.dev/files/66350afb-c5f2-4d92-b705-7bdc846b7714.jpeg',
    'https://cdn.poehali.dev/files/bfabeb17-fe5a-4a57-8306-df33558f9ec1.jpeg'
  ]

  return (
    <div className="min-h-screen bg-background">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-industrial uppercase tracking-wider">Массаж Булат</h1>
            <div className="hidden md:flex items-center gap-6">
              <a href="#services" className="text-foreground/80 hover:text-foreground transition-colors">Услуги</a>
              <a href="#prices" className="text-foreground/80 hover:text-foreground transition-colors">Прайс</a>
              <a href="#gallery" className="text-foreground/80 hover:text-foreground transition-colors">Галерея</a>
              <a href="#about" className="text-foreground/80 hover:text-foreground transition-colors">О мастере</a>
              <a href="#contacts" className="text-foreground/80 hover:text-foreground transition-colors">Контакты</a>
            </div>
            <Button className="bg-industrial hover:bg-industrial/90 text-white" onClick={() => setShowBooking(true)}>
              Записаться
            </Button>
          </div>
        </div>
      </nav>

      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-background/30 via-background/50 to-industrial/20" />
        <div 
          className="absolute inset-0 opacity-60"
          style={{
            backgroundImage: 'url(https://cdn.poehali.dev/files/e1832efa-4a2d-41cb-b464-51b3e1d6974b.jpeg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
        />
        <div className="container mx-auto px-4 relative z-10 text-center animate-fade-in">
          <h2 className="text-6xl md:text-8xl font-bold mb-6 text-white drop-shadow-lg uppercase tracking-tight">
            Массаж<br/>Лофт
          </h2>
          <p className="text-xl md:text-2xl text-white/90 drop-shadow-md mb-8 max-w-2xl mx-auto">
            Профессиональный массаж в атмосфере индустриального комфорта
          </p>
          <Button 
            size="lg" 
            className="bg-industrial hover:bg-industrial/90 text-white text-lg px-8 py-6"
            onClick={() => setShowBooking(true)}
          >
            Записаться на сеанс
          </Button>
        </div>
      </section>

      <section id="services" className="py-20 bg-terrace/5">
        <div className="container mx-auto px-4">
          <div className="border-4 border-industrial/30 rounded-2xl p-8 md:p-12">
            <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 uppercase">Услуги</h2>
            <p className="text-center text-foreground/70 mb-12 text-lg">Индивидуальный подход к каждому клиенту</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {services.map((service, index) => (
              <Card 
                key={index} 
                className="border-2 border-industrial/20 hover:border-industrial/40 transition-all hover:shadow-lg animate-fade-in hover-scale"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <CardHeader>
                  <div className="w-12 h-12 bg-industrial/10 rounded-lg flex items-center justify-center mb-4">
                    <Icon name={service.icon} className="text-industrial" size={24} />
                  </div>
                  <CardTitle className="text-xl">{service.title}</CardTitle>
                  <CardDescription>{service.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
            </div>
          </div>
        </div>
      </section>

      <section id="prices" className="py-20">
        <div className="container mx-auto px-4">
          <div className="border-4 border-industrial/30 rounded-2xl p-8 md:p-12">
            <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 uppercase">Прайс</h2>
            <p className="text-center text-foreground/70 mb-12 text-lg">Прозрачные цены без скрытых платежей</p>
            <div className="max-w-3xl mx-auto">
            <Accordion type="single" collapsible className="space-y-4">
              {services.map((service, index) => (
                <AccordionItem 
                  key={index} 
                  value={`item-${index}`}
                  className="border-2 border-industrial/20 rounded-lg px-6 animate-fade-in"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <AccordionTrigger className="text-lg font-semibold hover:no-underline">
                    <div className="flex items-center gap-3">
                      <Icon name={service.icon} className="text-industrial" size={20} />
                      {service.title}
                    </div>
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="space-y-3 pt-4">
                      {service.prices.map((price, idx) => (
                        <div key={idx} className="flex justify-between items-center py-2 border-b border-border last:border-0">
                          <span className="text-foreground/80">{price.duration}</span>
                          <span className="text-xl font-bold text-industrial">{price.price}</span>
                        </div>
                      ))}
                      <Button 
                        className="w-full mt-4 bg-industrial hover:bg-industrial/90 text-white"
                        onClick={() => {
                          setSelectedService(service.title)
                          setShowBooking(true)
                        }}
                      >
                        Записаться
                      </Button>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
            </div>
          </div>
        </div>
      </section>

      <section id="gallery" className="py-20 bg-terrace/5">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 uppercase">Галерея</h2>
          <p className="text-center text-foreground/70 mb-12 text-lg">Атмосфера наших массажных комнат</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {gallery.map((image, index) => (
              <div 
                key={index} 
                className="relative aspect-square overflow-hidden rounded-lg animate-fade-in hover-scale cursor-pointer"
                style={{ animationDelay: `${index * 100}ms` }}
                onClick={() => setSelectedImage(image)}
              >
                <img 
                  src={image} 
                  alt={`Галерея ${index + 1}`}
                  className="w-full h-full object-cover"
                />
              </div>
            ))}
          </div>
          
          {selectedImage && (
            <div 
              className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fade-in"
              onClick={() => setSelectedImage(null)}
            >
              <button 
                className="absolute top-4 right-4 text-white hover:text-white/80 transition-colors"
                onClick={() => setSelectedImage(null)}
              >
                <Icon name="X" size={32} />
              </button>
              <img 
                src={selectedImage} 
                alt="Увеличенное фото"
                className="max-w-full max-h-full object-contain rounded-lg"
                onClick={(e) => e.stopPropagation()}
              />
            </div>
          )}
        </div>
      </section>

      <section id="about" className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="animate-fade-in">
                <img 
                  src="https://cdn.poehali.dev/files/bfabeb17-fe5a-4a57-8306-df33558f9ec1.jpeg"
                  alt="Мастер Булат"
                  className="rounded-lg shadow-2xl"
                />
              </div>
              <div className="animate-fade-in" style={{ animationDelay: '200ms' }}>
                <h2 className="text-4xl md:text-5xl font-bold mb-6 uppercase">О мастере</h2>
                <h3 className="text-2xl font-semibold text-industrial mb-4">Булат</h3>
                <p className="text-foreground/80 text-lg leading-relaxed mb-4">
                  Сертифицированный массажист с опытом работы 4 года. Специализируюсь на классических и современных техниках массажа.
                </p>
                <p className="text-foreground/80 text-lg leading-relaxed mb-6">
                  Моя философия — индивидуальный подход к каждому клиенту. Я создаю атмосферу комфорта и релаксации в уникальном лофт-пространстве.
                </p>
                <div className="flex flex-wrap gap-3 mb-6">
                  <div className="flex items-center gap-2 bg-industrial/10 px-4 py-2 rounded-full">
                    <Icon name="Award" size={20} className="text-industrial" />
                    <span>4 года стажа</span>
                  </div>
                  <div className="flex items-center gap-2 bg-industrial/10 px-4 py-2 rounded-full">
                    <Icon name="Users" size={20} className="text-industrial" />
                    <span>100+ клиентов</span>
                  </div>
                  <div className="flex items-center gap-2 bg-industrial/10 px-4 py-2 rounded-full">
                    <Icon name="Star" size={20} className="text-industrial" />
                    <span>600+ сеансов</span>
                  </div>
                </div>
                <Button 
                  className="bg-industrial hover:bg-industrial/90 text-white"
                  onClick={() => setShowCertificates(true)}
                >
                  <Icon name="Award" size={20} className="mr-2" />
                  Посмотреть сертификаты
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="contacts" className="py-20 bg-terrace/5">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 uppercase">Контакты</h2>
          <p className="text-center text-foreground/70 mb-12 text-lg">Свяжитесь со мной удобным способом</p>
          <div className="max-w-2xl mx-auto">
            <Card className="border-2 border-industrial/20">
              <CardContent className="p-8 space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-industrial/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon name="MapPin" className="text-industrial" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg mb-1">Адрес</h3>
                    <p className="text-foreground/70">Будет указан при записи</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-industrial/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon name="Phone" className="text-industrial" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg mb-1">Телефон</h3>
                    <p className="text-foreground/70">+7 (XXX) XXX-XX-XX</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-industrial/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon name="Clock" className="text-industrial" size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg mb-1">Режим работы</h3>
                    <p className="text-foreground/70">Пн, Ср, Пт: 11:00 - 14:00 и 17:00 - 20:00</p>
                    <p className="text-foreground/70">Сб, Вс: 9:00 - 20:00</p>
                  </div>
                </div>
                <Button 
                  className="w-full bg-industrial hover:bg-industrial/90 text-white text-lg py-6"
                  onClick={() => setShowBooking(true)}
                >
                  <Icon name="Calendar" size={20} className="mr-2" />
                  Записаться онлайн
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      <footer className="bg-industrial text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-lg mb-2">Массаж Булат © 2025</p>
          <p className="text-white/70">Профессиональный массаж в стиле лофт</p>
        </div>
      </footer>

      {showCertificates && (
        <div 
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fade-in overflow-y-auto"
          onClick={() => setShowCertificates(false)}
        >
          <div className="container mx-auto max-w-5xl">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold text-white">Сертификаты</h2>
              <button 
                className="text-white hover:text-white/80 transition-colors"
                onClick={() => setShowCertificates(false)}
              >
                <Icon name="X" size={32} />
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" onClick={(e) => e.stopPropagation()}>
              <div className="bg-white/10 rounded-lg p-8 flex items-center justify-center text-white text-center min-h-[300px]">
                <div>
                  <Icon name="FileText" size={48} className="mx-auto mb-4 opacity-50" />
                  <p className="text-lg">Сертификат 1</p>
                  <p className="text-sm opacity-70 mt-2">Добавьте изображения сертификатов</p>
                </div>
              </div>
              <div className="bg-white/10 rounded-lg p-8 flex items-center justify-center text-white text-center min-h-[300px]">
                <div>
                  <Icon name="FileText" size={48} className="mx-auto mb-4 opacity-50" />
                  <p className="text-lg">Сертификат 2</p>
                  <p className="text-sm opacity-70 mt-2">Добавьте изображения сертификатов</p>
                </div>
              </div>
              <div className="bg-white/10 rounded-lg p-8 flex items-center justify-center text-white text-center min-h-[300px]">
                <div>
                  <Icon name="FileText" size={48} className="mx-auto mb-4 opacity-50" />
                  <p className="text-lg">Сертификат 3</p>
                  <p className="text-sm opacity-70 mt-2">Добавьте изображения сертификатов</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {showBooking && (
        <div 
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fade-in overflow-y-auto"
          onClick={() => setShowBooking(false)}
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
                  onClick={() => setShowBooking(false)}
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
                        // Пн, Ср, Пт: 11:00-14:00 и 17:00-20:00
                        for (let h = 11; h < 14; h++) {
                          times.push(`${h}:00`, `${h}:30`)
                        }
                        for (let h = 17; h < 20; h++) {
                          times.push(`${h}:00`, `${h}:30`)
                        }
                      } else {
                        // Сб, Вс: 9:00-20:00
                        for (let h = 9; h < 20; h++) {
                          times.push(`${h}:00`, `${h}:30`)
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
                  onClick={() => {
                    alert(`Запись создана!\nУслуга: ${selectedService}\nДата: ${selectedDate.toLocaleDateString('ru-RU')}\nВремя: ${selectedTime}\nИмя: ${customerName}\nТелефон: ${customerPhone}`)
                    setShowBooking(false)
                    setSelectedService(null)
                    setSelectedDate(null)
                    setSelectedTime(null)
                    setCustomerName('')
                    setCustomerPhone('')
                  }}
                >
                  Подтвердить запись
                </Button>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}