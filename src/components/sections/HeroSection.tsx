import { Button } from '@/components/ui/button'

interface HeroSectionProps {
  onBookingClick: () => void
}

export default function HeroSection({ onBookingClick }: HeroSectionProps) {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-background/30 via-background/50 to-industrial/20" />
      <div 
        className="absolute inset-0 opacity-60"
        style={{
          backgroundImage: 'url(https://cdn.poehali.dev/projects/f5643ba3-1fc8-40b9-b1c5-c401c23a1d03/files/368cc72e-dd55-44fa-8f0b-64cddbbefbf2.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />
      <div className="container mx-auto px-4 relative z-10 text-center animate-fade-in">
        <h2 className="text-6xl md:text-8xl font-bold mb-6 text-white drop-shadow-lg uppercase tracking-tight">
          Массаж<br/>Булат
        </h2>
        <p className="text-xl md:text-2xl text-white/90 drop-shadow-md mb-8 max-w-2xl mx-auto">
          Профессиональный массаж в атмосфере индустриального комфорта
        </p>
        <Button 
          size="lg" 
          className="bg-industrial hover:bg-industrial/90 text-white text-lg px-8 py-6"
          onClick={onBookingClick}
        >
          Записаться на сеанс
        </Button>
      </div>
    </section>
  )
}