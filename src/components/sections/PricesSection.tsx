import { Button } from '@/components/ui/button'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import Icon from '@/components/ui/icon'

interface Service {
  title: string
  description: string
  icon: string
  prices: { duration: string; price: string }[]
}

interface PricesSectionProps {
  services: Service[]
  onServiceSelect: (serviceTitle: string) => void
}

export default function PricesSection({ services, onServiceSelect }: PricesSectionProps) {
  return (
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
                        onClick={() => onServiceSelect(service.title)}
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
  )
}
