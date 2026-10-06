import { api } from './client'
import type { Supplier } from '../types'

export async function getSuppliers(): Promise<Supplier[]> {
  const { data } = await api.get<Supplier[]>('/suppliers/')
  return data
}

export async function createSupplier(input: Partial<Supplier>): Promise<Supplier> {
  const { data } = await api.post<Supplier>('/suppliers/', input)
  return data
}

export async function updateSupplier(id: number, input: Partial<Supplier>): Promise<Supplier> {
  const { data } = await api.put<Supplier>(`/suppliers/${id}`, input)
  return data
}

export async function deleteSupplier(id: number): Promise<void> {
  await api.delete(`/suppliers/${id}`)
}
