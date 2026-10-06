import { api } from './client'

export interface Settings {
  expiration_warning_days: number
}

export async function getSettings(): Promise<Settings> {
  const { data } = await api.get<Settings>('/settings/')
  return data
}

export async function updateSettings(days: number): Promise<Settings> {
  const { data } = await api.put<Settings>('/settings/', { expiration_warning_days: days })
  return data
}
