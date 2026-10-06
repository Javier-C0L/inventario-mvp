import { api } from './client'
import type { Category } from '../types'

export async function getCategories(): Promise<Category[]> {
  const { data } = await api.get<Category[]>('/categories/')
  return data
}

export async function createCategory(input: { name: string; description?: string }): Promise<Category> {
  const { data } = await api.post<Category>('/categories/', input)
  return data
}

export async function updateCategory(id: number, input: { name?: string; description?: string }): Promise<Category> {
  const { data } = await api.put<Category>(`/categories/${id}`, input)
  return data
}

export async function deleteCategory(id: number): Promise<void> {
  await api.delete(`/categories/${id}`)
}
