type ExpirationStatus = 'vigente' | 'proximo_a_vencer' | 'vencido' | 'sin_fecha'

const labels: Record<ExpirationStatus, string> = {
  vigente: 'Vigente',
  proximo_a_vencer: 'Próximo a vencer',
  vencido: 'Vencido',
  sin_fecha: 'Sin fecha',
}

const colors: Record<ExpirationStatus, string> = {
  vigente: 'bg-green-100 text-green-700',
  proximo_a_vencer: 'bg-yellow-100 text-yellow-700',
  vencido: 'bg-red-100 text-red-700',
  sin_fecha: 'bg-gray-200 text-gray-600',
}

export default function ExpirationBadge({ status }: { status: ExpirationStatus }) {
  return <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>{labels[status]}</span>
}
