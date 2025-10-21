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
              <div className="flex items-center justify-center gap-4 pt-4">
                <a 
                  href="https://vk.com/burynamass?from=groups" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="w-14 h-14 bg-[#0077FF] hover:bg-[#0066DD] rounded-lg flex items-center justify-center transition-colors"
                  aria-label="ВКонтакте"
                >
                  <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M15.07 2H8.93C3.33 2 2 3.33 2 8.93v6.14C2 20.67 3.33 22 8.93 22h6.14c5.6 0 6.93-1.33 6.93-6.93V8.93C22 3.33 20.67 2 15.07 2zm3.41 14.09h-1.44c-.46 0-.61-.37-1.44-1.2-.73-.7-1.04-.79-1.22-.79-.25 0-.32.07-.32.41v1.1c0 .3-.09.48-1.12.48-1.71 0-3.6-.97-4.93-2.78-2-2.63-2.55-4.61-2.55-5.01 0-.18.07-.35.41-.35h1.44c.31 0 .42.14.54.46.61 1.72 1.63 3.24 2.05 3.24.16 0 .23-.07.23-.48v-1.86c-.05-.98-.58-1.06-.58-1.41 0-.14.12-.28.32-.28h2.26c.26 0 .36.14.36.44v2.51c0 .26.12.36.19.36.16 0 .29-.1.58-.39 1.38-1.55 2.37-3.93 2.37-3.93.13-.28.27-.39.58-.39h1.44c.35 0 .42.18.35.44-.18.86-1.98 3.93-1.98 3.93-.13.23-.18.33 0 .59.13.18.55.54.83.87.52.52 1.38 1.43 1.53 1.88.08.24-.04.37-.34.37z"/>
                  </svg>
                </a>
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