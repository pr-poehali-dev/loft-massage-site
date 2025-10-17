import { Button } from '@/components/ui/button'

interface HeaderProps {
  onBookingClick: () => void
}

export default function Header({ onBookingClick }: HeaderProps) {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-industrial uppercase tracking-wider">Массаж Булат</h1>
          <div className="hidden md:flex items-center gap-6">
            <a href="#services" className="text-foreground/80 hover:text-foreground transition-colors">Услуги</a>
            <a href="#prices" className="text-foreground/80 hover:text-foreground transition-colors">Прайс</a>
            <a href="#gallery" className="text-foreground/80 hover:text-foreground transition-colors">Галерея</a>
            <a href="#about" className="text-foreground/80 hover:text-foreground transition-colors">О мастере</a>
            <a href="#contacts" className="text-foreground/80 hover:text-foreground transition-colors">Контакты</a>
          </div>
          <Button className="bg-industrial hover:bg-industrial/90 text-white" onClick={onBookingClick}>
            Записаться
          </Button>
        </div>
      </div>
    </nav>
  )
}
