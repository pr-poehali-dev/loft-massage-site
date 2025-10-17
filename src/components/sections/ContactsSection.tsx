import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import Icon from '@/components/ui/icon'

interface ContactsSectionProps {
  onBookingClick: () => void
}

export default function ContactsSection({ onBookingClick }: ContactsSectionProps) {
  return (
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
                onClick={onBookingClick}
              >
                <Icon name="Calendar" size={20} className="mr-2" />
                Записаться онлайн
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
