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
import { API_ENDPOINTS } from '@/config/api'

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
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/cc9b3251-09fb-4fd2-a768-a79a504cbb19.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/f5b1e1b2-8a00-43d6-8b1a-bc9e8e431309.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/d2438036-67a2-4140-8a60-2d8b042ebb92.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/0c9349a7-7c9b-4f9e-9cc1-a369db38285e.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/d05123ae-32f8-4552-93a3-ae0b33b9d8af.jpg'
  ]

  const handleServiceSelect = (serviceTitle: string) => {
    setSelectedService(serviceTitle)
    setShowBooking(true)
  }

  const handleConfirmBooking = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.bookings, {
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