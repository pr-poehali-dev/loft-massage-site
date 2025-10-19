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
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/dbbf1427-3c7a-4499-b8b0-f5114e651f9b.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/094691cf-cfab-407c-9a70-aed633cdaddd.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/425e9132-8315-49f7-bd31-95901370bf2c.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/22c0d83c-29d8-4d7e-aa66-080e7e458362.jpg',
    'https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/54c69b2e-a93c-4c22-998b-1628c514031f.jpg'
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