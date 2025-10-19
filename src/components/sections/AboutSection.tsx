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
                src="https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/d65677da-2fb4-4931-ac5d-fab256e78b29.jpg"
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
                onClick={onShowCertificates}
              >
                <Icon name="Award" size={20} className="mr-2" />
                Посмотреть сертификаты
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}