import { FormEvent, useEffect, useState } from 'react'
import { getSettings, updateSettings } from '../api/settings'

export default function SettingsPage() {
  const [days, setDays] = useState(30)
  const [notice, setNotice] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getSettings().then((s) => setDays(s.expiration_warning_days)).catch((e) => setError(e.message))
  }, [])

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setNotice(null)
    try {
      const s = await updateSettings(days)
      setDays(s.expiration_warning_days)
      setNotice('Configuración guardada')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al guardar')
    }
  }

  return (
    <div className="max-w-xl">
      <h2 className="text-xl font-semibold mb-4">Configuración</h2>
      {notice && <p className="text-green-600 mb-3">{notice}</p>}
      {error && <p className="text-red-600 mb-3">{error}</p>}
      <form onSubmit={submit} className="bg-white p-6 rounded-lg shadow flex flex-col gap-4">
        <label className="text-sm flex flex-col">
          Días de anticipación para "próximo a vencer"
          <input type="number" min={0} max={365} className="border rounded px-3 py-2 mt-1" value={days} onChange={(e) => setDays(Number(e.target.value))} />
        </label>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded self-start">Guardar</button>
      </form>
    </div>
  )
}
