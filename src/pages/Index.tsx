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
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/a1e94e4d-1aaf-4dc5-bfe7-2c4ecf3c83ac.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/9f33cf54-87ee-4a7a-a5fa-7ee5aa53a076.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/e1ec8a51-ea17-4950-8f4e-e6a6a7ce2c52.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/b82ae8a2-9e0c-42cd-98eb-d79f1a8d2e40.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/8dcbf1e0-3a94-40c4-a41f-a8f0e8ab8aaa.jpg'
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