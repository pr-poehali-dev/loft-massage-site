import Icon from '@/components/ui/icon'

interface GallerySectionProps {
  gallery: string[]
  onImageClick: (image: string) => void
  selectedImage: string | null
  onCloseImage: () => void
}

export default function GallerySection({ gallery, onImageClick, selectedImage, onCloseImage }: GallerySectionProps) {
  return (
    <section id="gallery" className="py-20 bg-terrace/5">
      <div className="container mx-auto px-4">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 uppercase">Галерея</h2>
        <p className="text-center text-foreground/70 mb-12 text-lg">Атмосфера наших массажных комнат</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {gallery.map((image, index) => (
            <div 
              key={index} 
              className="relative aspect-square overflow-hidden rounded-lg animate-fade-in hover-scale cursor-pointer"
              style={{ animationDelay: `${index * 100}ms` }}
              onClick={() => onImageClick(image)}
            >
              <img 
                src={image} 
                alt={`Галерея ${index + 1}`}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
        
        {selectedImage && (
          <div 
            className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fade-in"
            onClick={onCloseImage}
          >
            <button 
              className="absolute top-4 right-4 text-white hover:text-white/80 transition-colors"
              onClick={onCloseImage}
            >
              <Icon name="X" size={32} />
            </button>
            <img 
              src={selectedImage} 
              alt="Увеличенное фото"
              className="max-w-full max-h-full object-contain rounded-lg"
              onClick={(e) => e.stopPropagation()}
            />
          </div>
        )}
      </div>
    </section>
  )
}
