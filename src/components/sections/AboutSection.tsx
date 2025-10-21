import { Button } from '@/components/ui/button'
import Icon from '@/components/ui/icon'

interface AboutSectionProps {
  onShowCertificates: () => void
}

export default function AboutSection({ onShowCertificates }: AboutSectionProps) {
  return (
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
              <div className="flex gap-3">
                <Button 
                  className="bg-industrial hover:bg-industrial/90 text-white"
                  onClick={onShowCertificates}
                >
                  <Icon name="Award" size={20} className="mr-2" />
                  Посмотреть сертификаты
                </Button>
                <a 
                  href="https://vk.com/burynamass?from=groups" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="w-12 h-12 bg-[#C4A574] hover:bg-[#B89560] rounded-lg flex items-center justify-center transition-colors flex-shrink-0"
                  aria-label="ВКонтакте"
                >
                  <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M15.07 2H8.93C3.33 2 2 3.33 2 8.93v6.14C2 20.67 3.33 22 8.93 22h6.14c5.6 0 6.93-1.33 6.93-6.93V8.93C22 3.33 20.67 2 15.07 2zm3.41 14.09h-1.44c-.46 0-.61-.37-1.44-1.2-.73-.7-1.04-.79-1.22-.79-.25 0-.32.07-.32.41v1.1c0 .3-.09.48-1.12.48-1.71 0-3.6-.97-4.93-2.78-2-2.63-2.55-4.61-2.55-5.01 0-.18.07-.35.41-.35h1.44c.31 0 .42.14.54.46.61 1.72 1.63 3.24 2.05 3.24.16 0 .23-.07.23-.48v-1.86c-.05-.98-.58-1.06-.58-1.41 0-.14.12-.28.32-.28h2.26c.26 0 .36.14.36.44v2.51c0 .26.12.36.19.36.16 0 .29-.1.58-.39 1.38-1.55 2.37-3.93 2.37-3.93.13-.28.27-.39.58-.39h1.44c.35 0 .42.18.35.44-.18.86-1.98 3.93-1.98 3.93-.13.23-.18.33 0 .59.13.18.55.54.83.87.52.52 1.38 1.43 1.53 1.88.08.24-.04.37-.34.37z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}