import { FormEvent, useEffect, useState } from 'react'
import { createCategory, deleteCategory, getCategories, updateCategory } from '../api/categories'
import Modal from '../components/ui/Modal'
import type { Category } from '../types'

export default function CategoriesPage() {
  const [items, setItems] = useState<Category[]>([])
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [editing, setEditing] = useState<Category | null>(null)
  const [toDelete, setToDelete] = useState<Category | null>(null)
  const [error, setError] = useState<string | null>(null)

  const load = () => getCategories().then(setItems).catch((e) => setError(e.message))
  useEffect(() => { load() }, [])

  const openEdit = (c: Category) => { setEditing(c); setName(c.name); setDescription(c.description ?? '') }

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!name.trim()) { setError('El nombre es obligatorio'); return }
    try {
      if (editing) await updateCategory(editing.id, { name, description: description || undefined })
      else await createCategory({ name, description: description || undefined })
      setEditing(null); setName(''); setDescription(''); load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error')
    }
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Categorías</h2>
      {error && <p className="text-red-600 mb-3">{error}</p>}
      <form onSubmit={submit} className="bg-white p-4 rounded-lg shadow mb-4 flex gap-3 flex-wrap">
        <input className="border rounded px-3 py-2 flex-1" placeholder="Nombre" value={name} onChange={(e) => setName(e.target.value)} />
        <input className="border rounded px-3 py-2 flex-1" placeholder="Descripción" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">{editing ? 'Actualizar' : 'Agregar'}</button>
        {editing && <button type="button" className="border px-4 py-2 rounded" onClick={() => { setEditing(null); setName(''); setDescription('') }}>Cancelar</button>}
      </form>
      <table className="w-full bg-white rounded-lg shadow text-sm">
        <thead className="bg-gray-100 text-left"><tr><th className="p-3">Nombre</th><th className="p-3">Descripción</th><th className="p-3"></th></tr></thead>
        <tbody>
          {items.map((c) => (
            <tr key={c.id} className="border-t">
              <td className="p-3">{c.name}</td>
              <td className="p-3">{c.description ?? '—'}</td>
              <td className="p-3 flex gap-3">
                <button className="text-gray-600" onClick={() => openEdit(c)}>Editar</button>
                <button className="text-red-600" onClick={() => setToDelete(c)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {toDelete && (
        <Modal title="Eliminar categoría" onClose={() => setToDelete(null)}>
          <p className="mb-4">¿Eliminar <strong>{toDelete.name}</strong>?</p>
          <div className="flex justify-end gap-3">
            <button className="border px-4 py-2 rounded" onClick={() => setToDelete(null)}>Cancelar</button>
            <button className="bg-red-600 text-white px-4 py-2 rounded" onClick={async () => { await deleteCategory(toDelete.id); setToDelete(null); load() }}>Eliminar</button>
          </div>
        </Modal>
      )}
    </div>
  )
}
