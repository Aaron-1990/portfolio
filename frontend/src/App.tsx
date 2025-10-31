/**
 * App Component
 * 
 * Componente principal con navegación y layout
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from './api/client'
import PortfolioDashboard from './components/portfolio/PortfolioDashboard'
import './App.css'

function App() {
  const [selectedPortfolioId, setSelectedPortfolioId] = useState<number | null>(null)

  // Query para obtener lista de portafolios
  const { data: portfolios, isLoading, error } = useQuery({
    queryKey: ['portfolios'],
    queryFn: api.portfolios.list,
  })

  // Query para precios actuales
  const { data: prices } = useQuery({
    queryKey: ['prices'],
    queryFn: api.prices.getLatest,
    refetchInterval: 5 * 60 * 1000, // Actualizar cada 5 minutos
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando portafolios...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-5xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Error de Conexión</h2>
          <p className="text-gray-600 mb-4">No se pudo conectar con el backend</p>
          <p className="text-sm text-gray-500">Asegúrate de que el servidor esté corriendo en http://localhost:8000</p>
        </div>
      </div>
    )
  }

  // Si no hay portafolios, mostrar pantalla de bienvenida
  if (!portfolios || portfolios.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">📊 Portfolio Tracker</h1>
          <p className="text-gray-600 mb-8">No hay portafolios creados aún</p>
          <button
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
            onClick={() => alert('Crear portafolio - TODO: Implementar modal')}
          >
            Crear Primer Portafolio
          </button>
        </div>
      </div>
    )
  }

  // Si no hay portfolio seleccionado, seleccionar el primero
  const currentPortfolio = selectedPortfolioId 
    ? portfolios.find(p => p.id === selectedPortfolioId) 
    : portfolios[0]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">📊 Portfolio Tracker</h1>
              <select
                className="ml-4 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={currentPortfolio?.id || ''}
                onChange={(e) => setSelectedPortfolioId(Number(e.target.value))}
              >
                {portfolios.map((p: any) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-center space-x-4">
              {prices && (
                <div className="text-sm text-gray-600">
                  <span className="font-medium">VOO:</span> ${prices.VOO?.toFixed(2)}
                  <span className="ml-4 font-medium">BTC:</span> ${prices.BTC?.toFixed(0)}
                </div>
              )}
              <button
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
                onClick={() => alert('Actualizar precios - TODO')}
              >
                🔄 Actualizar
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentPortfolio && (
          <PortfolioDashboard 
            portfolio={currentPortfolio}
            prices={prices || {}}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-gray-500 text-sm">
          <p>Portfolio Tracker v1.0.0 | Built with ❤️ using FastAPI + React</p>
        </div>
      </footer>
    </div>
  )
}

export default App
