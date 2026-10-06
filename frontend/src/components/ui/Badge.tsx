import type { ProductStatus } from '../../types'

const labels: Record<ProductStatus, string> = {
  vigente: 'Vigente',
  proximo_a_vencer: 'Próximo a vencer',
  vencido: 'Vencido',
  agotado: 'Agotado',
}

const colors: Record<ProductStatus, string> = {
  vigente: 'bg-green-100 text-green-700',
  proximo_a_vencer: 'bg-yellow-100 text-yellow-700',
  vencido: 'bg-red-100 text-red-700',
  agotado: 'bg-gray-200 text-gray-700',
}

export default function Badge({ status }: { status: ProductStatus }) {
  return <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>{labels[status]}</span>
}
