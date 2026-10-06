import { FormEvent, useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createProduct, getProduct, updateProduct } from '../api/products'
import { getCategories } from '../api/categories'
import { getSuppliers } from '../api/suppliers'
import type { Category, Product, Supplier } from '../types'

const empty = {
  sku: '', name: '', description: '', category_id: '' as string | number, supplier_id: '' as string | number,
  quantity: 0, unit: 'unidad', min_stock: 0, purchase_price: 0, sale_price: 0,
  entry_date: new Date().toISOString().slice(0, 10), expiration_date: '', location: '', status: 'vigente',
}

export default function ProductFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState({ ...empty })
  const [categories, setCategories] = useState<Category[]>([])
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getCategories().then(setCategories)
    getSuppliers().then(setSuppliers)
    if (id) {
      getProduct(Number(id)).then((p) => setForm({
        ...empty, ...p,
        category_id: p.category_id ?? '', supplier_id: p.supplier_id ?? '',
        description: p.description ?? '', expiration_date: p.expiration_date ?? '', location: p.location ?? '',
      }))
    }
  }, [id])

  const set = (key: string, value: string | number) => setForm((f) => ({ ...f, [key]: value }))

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!form.sku || !form.name) {
      setError('SKU y nombre son obligatorios')
      return
    }
    const payload = {
      ...form,
      category_id: form.category_id === '' ? null : Number(form.category_id),
      supplier_id: form.supplier_id === '' ? null : Number(form.supplier_id),
      description: form.description || null,
      expiration_date: form.expiration_date || null,
      location: form.location || null,
      quantity: Number(form.quantity),
      min_stock: Number(form.min_stock),
      purchase_price: Number(form.purchase_price),
      sale_price: Number(form.sale_price),
      status: form.status as Product['status'],
    }
    try {
      if (id) await updateProduct(Number(id), payload)
      else await createProduct(payload)
      navigate('/productos')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al guardar')
    }
  }

  return (
    <div className="max-w-3xl">
      <h2 className="text-xl font-semibold mb-4">{id ? 'Editar producto' : 'Nuevo producto'}</h2>
      {error && <p className="text-red-600 mb-3">{error}</p>}
      <form onSubmit={submit} className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-white p-6 rounded-lg shadow">
        <label className="flex flex-col text-sm">SKU *<input className="border rounded px-3 py-2 mt-1" value={form.sku} onChange={(e) => set('sku', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Nombre *<input className="border rounded px-3 py-2 mt-1" value={form.name} onChange={(e) => set('name', e.target.value)} /></label>
        <label className="flex flex-col text-sm md:col-span-2">Descripción<textarea className="border rounded px-3 py-2 mt-1" value={form.description} onChange={(e) => set('description', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Categoría
          <select className="border rounded px-3 py-2 mt-1" value={form.category_id} onChange={(e) => set('category_id', e.target.value)}>
            <option value="">Sin categoría</option>
            {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </label>
        <label className="flex flex-col text-sm">Proveedor
          <select className="border rounded px-3 py-2 mt-1" value={form.supplier_id} onChange={(e) => set('supplier_id', e.target.value)}>
            <option value="">Sin proveedor</option>
            {suppliers.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </label>
        <label className="flex flex-col text-sm">Cantidad<input type="number" min={0} className="border rounded px-3 py-2 mt-1" value={form.quantity} onChange={(e) => set('quantity', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Unidad<input className="border rounded px-3 py-2 mt-1" value={form.unit} onChange={(e) => set('unit', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Stock mínimo<input type="number" min={0} className="border rounded px-3 py-2 mt-1" value={form.min_stock} onChange={(e) => set('min_stock', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Precio compra<input type="number" step="0.01" min={0} className="border rounded px-3 py-2 mt-1" value={form.purchase_price} onChange={(e) => set('purchase_price', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Precio venta<input type="number" step="0.01" min={0} className="border rounded px-3 py-2 mt-1" value={form.sale_price} onChange={(e) => set('sale_price', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Fecha ingreso<input type="date" className="border rounded px-3 py-2 mt-1" value={form.entry_date} onChange={(e) => set('entry_date', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Fecha vencimiento<input type="date" className="border rounded px-3 py-2 mt-1" value={form.expiration_date} onChange={(e) => set('expiration_date', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Ubicación<input className="border rounded px-3 py-2 mt-1" value={form.location} onChange={(e) => set('location', e.target.value)} /></label>
        <label className="flex flex-col text-sm">Estado
          <select className="border rounded px-3 py-2 mt-1" value={form.status} onChange={(e) => set('status', e.target.value)}>
            <option value="vigente">Vigente</option>
            <option value="proximo_a_vencer">Próximo a vencer</option>
            <option value="vencido">Vencido</option>
            <option value="agotado">Agotado</option>
          </select>
        </label>
        <div className="md:col-span-2 flex justify-end gap-3 mt-2">
          <button type="button" className="border px-4 py-2 rounded" onClick={() => navigate('/productos')}>Cancelar</button>
          <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Guardar</button>
        </div>
      </form>
    </div>
  )
}
