import Icon from '@/components/ui/icon'

interface CertificatesModalProps {
  show: boolean
  onClose: () => void
}

export default function CertificatesModal({ show, onClose }: CertificatesModalProps) {
  if (!show) return null

  return (
    <div 
      className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fade-in overflow-y-auto"
      onClick={onClose}
    >
      <div className="container mx-auto max-w-5xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-white">Сертификаты</h2>
          <button 
            className="text-white hover:text-white/80 transition-colors"
            onClick={onClose}
          >
            <Icon name="X" size={32} />
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" onClick={(e) => e.stopPropagation()}>
          <div className="bg-white/10 rounded-lg p-8 flex items-center justify-center text-white text-center min-h-[300px]">
            <div>
              <Icon name="FileText" size={48} className="mx-auto mb-4 opacity-50" />
              <p className="text-lg">Сертификат 1</p>
              <p className="text-sm opacity-70 mt-2">Добавьте изображения сертификатов</p>
            </div>
          </div>
          <div className="bg-white/10 rounded-lg p-8 flex items-center justify-center text-white text-center min-h-[300px]">
            <div>
              <Icon name="FileText" size={48} className="mx-auto mb-4 opacity-50" />
              <p className="text-lg">Сертификат 2</p>
              <p className="text-sm opacity-70 mt-2">Добавьте изображения сертификатов</p>
            </div>
          </div>
          <div className="bg-white/10 rounded-lg p-8 flex items-center justify-center text-white text-center min-h-[300px]">
            <div>
              <Icon name="FileText" size={48} className="mx-auto mb-4 opacity-50" />
              <p className="text-lg">Сертификат 3</p>
              <p className="text-sm opacity-70 mt-2">Добавьте изображения сертификатов</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
