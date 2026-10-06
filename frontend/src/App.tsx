import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Sidebar from './components/layout/Sidebar'
import ProductsPage from './pages/ProductsPage'
import ProductFormPage from './pages/ProductFormPage'
import ProductDetailPage from './pages/ProductDetailPage'
import CategoriesPage from './pages/CategoriesPage'
import SuppliersPage from './pages/SuppliersPage'
import PlaceholderPage from './pages/PlaceholderPage'
import MovementsPage from './pages/MovementsPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <main className="flex-1 p-6">
          <Routes>
            <Route path="/" element={<PlaceholderPage title="Dashboard" />} />
            <Route path="/productos" element={<ProductsPage />} />
            <Route path="/productos/nuevo" element={<ProductFormPage />} />
            <Route path="/productos/:id" element={<ProductDetailPage />} />
            <Route path="/productos/:id/editar" element={<ProductFormPage />} />
            <Route path="/movimientos" element={<MovementsPage />} />
            <Route path="/categorias" element={<CategoriesPage />} />
            <Route path="/proveedores" element={<SuppliersPage />} />
            <Route path="/configuracion" element={<SettingsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
