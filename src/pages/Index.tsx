import { useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import HeroSection from '@/components/sections/HeroSection'
import ServicesSection from '@/components/sections/ServicesSection'
import PricesSection from '@/components/sections/PricesSection'
import GallerySection from '@/components/sections/GallerySection'
import AboutSection from '@/components/sections/AboutSection'
import ContactsSection from '@/components/sections/ContactsSection'
import CertificatesModal from '@/components/modals/CertificatesModal'
import BookingModal from '@/components/modals/BookingModal'

export default function Index() {
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
      prices: [{ duration: '30 минут', price: '1600₽' }]
    },
    {
      title: 'Успокаивающий массаж спина',
      description: 'Этот массаж создан специально для тех, кто нуждается в эмоциональной разгрузке. Мягкие, плавные движения помогут вам расслабиться, снять стресс и восстановить внутреннюю гармонию. Идеален после напряженного дня',
      icon: 'Sparkles',
      prices: [{ duration: '30 минут', price: '1600₽' }]
    },
    {
      title: 'Классический массаж тело',
      description: 'Комплексная проработка всего тела. Улучшает кровообращение, снимает мышечное напряжение и дарит чувство обновления. Вы почувствуете как каждая клеточка вашего тела наполняется энергией и жизненной силой',
      icon: 'User',
      prices: [{ duration: '60 минут', price: '2600₽' }]
    },
    {
      title: 'Расслабляющий массаж тела',
      description: 'Массаж позволяющий вам собраться с мыслями, отпустить все ваши тревоги и заботы. Отдохните телом и душой пока руки мастера творят свое волшебство',
      icon: 'Heart',
      prices: [{ duration: '60 минут', price: '2600₽' }]
    }
  ]

  const gallery = [
    'https://cdn.poehali.dev/files/e1832efa-4a2d-41cb-b464-51b3e1d6974b.jpeg',
    'https://cdn.poehali.dev/files/ca89434b-6670-4b10-9942-f9b1f36a7f7a.jpeg',
    'https://cdn.poehali.dev/files/73991933-3d6d-476a-be3e-da7f0c43bc38.jpeg',
    'https://cdn.poehali.dev/files/66350afb-c5f2-4d92-b705-7bdc846b7714.jpeg',
    'https://cdn.poehali.dev/files/bfabeb17-fe5a-4a57-8306-df33558f9ec1.jpeg'
  ]

  const handleServiceSelect = (serviceTitle: string) => {
    setSelectedService(serviceTitle)
    setShowBooking(true)
  }

  const handleConfirmBooking = async () => {
    try {
      const response = await fetch('https://functions.poehali.dev/44725468-4f39-4361-bc48-b76fb53f5e04', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service: selectedService,
          booking_date: selectedDate?.toISOString().split('T')[0],
          booking_time: selectedTime,
          customer_name: customerName,
          customer_phone: customerPhone
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        alert(`✅ Запись создана!\n\nУслуга: ${selectedService}\nДата: ${selectedDate?.toLocaleDateString('ru-RU')}\nВремя: ${selectedTime}\nИмя: ${customerName}\n\nДля отмены используйте ссылку из SMS`)
        setShowBooking(false)
        setSelectedService(null)
        setSelectedDate(null)
        setSelectedTime(null)
        setCustomerName('')
        setCustomerPhone('')
      } else {
        alert(`Ошибка: ${data.error || 'Не удалось создать запись'}`)
      }
    } catch (error) {
      alert('Ошибка соединения с сервером')
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Header onBookingClick={() => setShowBooking(true)} />
      
      <HeroSection onBookingClick={() => setShowBooking(true)} />
      
      <ServicesSection services={services} />
      
      <PricesSection services={services} onServiceSelect={handleServiceSelect} />
      
      <GallerySection 
        gallery={gallery}
        onImageClick={setSelectedImage}
        selectedImage={selectedImage}
        onCloseImage={() => setSelectedImage(null)}
      />
      
      <AboutSection onShowCertificates={() => setShowCertificates(true)} />
      
      <ContactsSection onBookingClick={() => setShowBooking(true)} />
      
      <Footer />

      <CertificatesModal 
        show={showCertificates}
        onClose={() => setShowCertificates(false)}
      />

      <BookingModal
        show={showBooking}
        onClose={() => setShowBooking(false)}
        services={services}
        selectedService={selectedService}
        setSelectedService={setSelectedService}
        selectedDate={selectedDate}
        setSelectedDate={setSelectedDate}
        selectedTime={selectedTime}
        setSelectedTime={setSelectedTime}
        customerName={customerName}
        setCustomerName={setCustomerName}
        customerPhone={customerPhone}
        setCustomerPhone={setCustomerPhone}
        onConfirmBooking={handleConfirmBooking}
      />
    </div>
  )
}
