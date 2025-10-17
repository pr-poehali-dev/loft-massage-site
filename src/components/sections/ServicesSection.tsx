import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Icon from '@/components/ui/icon'

interface Service {
  title: string
  description: string
  icon: string
  prices: { duration: string; price: string }[]
}

interface ServicesSectionProps {
  services: Service[]
}

export default function ServicesSection({ services }: ServicesSectionProps) {
  return (
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
  )
}
