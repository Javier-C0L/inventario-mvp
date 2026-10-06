import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/productos', label: 'Productos' },
  { to: '/movimientos', label: 'Movimientos' },
  { to: '/categorias', label: 'Categorías' },
  { to: '/proveedores', label: 'Proveedores' },
  { to: '/configuracion', label: 'Configuración' },
]

export default function Sidebar() {
  return (
    <aside className="w-56 bg-gray-900 text-gray-200 min-h-screen p-4 flex flex-col gap-1">
      <h1 className="text-xl font-bold mb-6 text-white">Inventario</h1>
      {links.map((l) => (
        <NavLink key={l.to} to={l.to} end={l.to === '/'}
          className={({ isActive }) => `px-3 py-2 rounded ${isActive ? 'bg-gray-700 text-white' : 'hover:bg-gray-800'}`}>
          {l.label}
        </NavLink>
      ))}
    </aside>
  )
}
