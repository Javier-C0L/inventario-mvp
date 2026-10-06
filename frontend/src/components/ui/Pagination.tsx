interface Props {
  total: number
  limit: number
  offset: number
  onPage: (offset: number) => void
}

export default function Pagination({ total, limit, offset, onPage }: Props) {
  const page = Math.floor(offset / limit) + 1
  const pages = Math.max(1, Math.ceil(total / limit))
  return (
    <div className="flex items-center justify-between text-sm text-gray-600 mt-4">
      <span>Total: {total}</span>
      <div className="flex gap-2 items-center">
        <button className="px-3 py-1 border rounded disabled:opacity-40" disabled={offset === 0} onClick={() => onPage(Math.max(0, offset - limit))}>Anterior</button>
        <span>Página {page} de {pages}</span>
        <button className="px-3 py-1 border rounded disabled:opacity-40" disabled={offset + limit >= total} onClick={() => onPage(offset + limit)}>Siguiente</button>
      </div>
    </div>
  )
}
