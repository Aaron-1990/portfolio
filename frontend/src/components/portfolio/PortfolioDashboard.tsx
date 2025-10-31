/**
 * Portfolio Dashboard Component
 * 
 * Muestra vista completa del portafolio con gráficas y métricas
 */

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

interface PortfolioDashboardProps {
  portfolio: any
  prices: Record<string, number>
}

// Colores para cada activo
const COLORS: Record<string, string> = {
  VOO: '#3B82F6', // Blue
  VGT: '#8B5CF6', // Purple
  BTC: '#F59E0B', // Orange
  ETH: '#10B981', // Green
}

const PortfolioDashboard = ({ portfolio, prices }: PortfolioDashboardProps) => {
  // Calcular distribución actual basado en precios
  const calculateDistribution = () => {
    const holdings = [
      { ticker: 'VOO', quantity: 0.85, avgPrice: 490 },
      { ticker: 'VGT', quantity: 0.75, avgPrice: 560 },
      { ticker: 'BTC', quantity: 0.015, avgPrice: 45000 },
      { ticker: 'ETH', quantity: 0.08, avgPrice: 2200 },
    ]

    return holdings.map(holding => {
      const currentPrice = prices[holding.ticker] || holding.avgPrice
      const currentValue = holding.quantity * currentPrice
      const invested = holding.quantity * holding.avgPrice
      const gainLoss = currentValue - invested
      const gainLossPercent = (gainLoss / invested) * 100

      return {
        ticker: holding.ticker,
        quantity: holding.quantity,
        avgPrice: holding.avgPrice,
        currentPrice,
        currentValue,
        invested,
        gainLoss,
        gainLossPercent,
      }
    })
  }

  const holdings = calculateDistribution()
  const totalValue = holdings.reduce((sum, h) => sum + h.currentValue, 0)
  const totalInvested = holdings.reduce((sum, h) => sum + h.invested, 0)
  const totalGainLoss = totalValue - totalInvested
  const totalGainLossPercent = (totalGainLoss / totalInvested) * 100

  // Datos para pie chart
  const pieData = holdings.map(h => ({
    name: h.ticker,
    value: h.currentValue,
    percent: (h.currentValue / totalValue) * 100,
  }))

  return (
    <div className="space-y-6">
      {/* Header con métricas principales */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">{portfolio.name}</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Valor Total</p>
            <p className="text-3xl font-bold text-gray-900">
              ${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </p>
            <p className="text-sm text-gray-500 mt-1">USD</p>
          </div>

          <div className={`rounded-lg p-4 ${totalGainLoss >= 0 ? 'bg-green-50' : 'bg-red-50'}`}>
            <p className="text-sm text-gray-600 mb-1">Ganancia/Pérdida</p>
            <p className={`text-3xl font-bold ${totalGainLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {totalGainLoss >= 0 ? '+' : ''}${totalGainLoss.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </p>
            <p className={`text-sm font-medium mt-1 ${totalGainLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {totalGainLoss >= 0 ? '+' : ''}{totalGainLossPercent.toFixed(2)}%
            </p>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Total Invertido</p>
            <p className="text-3xl font-bold text-gray-900">
              ${totalInvested.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </p>
            <p className="text-sm text-gray-500 mt-1">USD</p>
          </div>
        </div>
      </div>

      {/* Distribución Actual */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Distribución Actual</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name} (${entry.percent.toFixed(1)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
                ))}
              </Pie>
              <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Target vs Actual */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Target vs Actual</h3>
          <div className="space-y-4">
            {holdings.map(h => {
              const targetPercent = parseFloat(portfolio[`target_${h.ticker.toLowerCase()}_percent`] || 0)
              const actualPercent = (h.currentValue / totalValue) * 100
              const diff = actualPercent - targetPercent

              return (
                <div key={h.ticker}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-medium text-gray-700">{h.ticker}</span>
                    <span className="text-sm text-gray-600">
                      {actualPercent.toFixed(1)}% / {targetPercent.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="h-2 rounded-full"
                        style={{
                          width: `${actualPercent}%`,
                          backgroundColor: COLORS[h.ticker],
                        }}
                      />
                    </div>
                    <span className={`text-xs font-medium ${Math.abs(diff) < 2 ? 'text-green-600' : 'text-yellow-600'}`}>
                      {diff >= 0 ? '+' : ''}{diff.toFixed(1)}%
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Detalle por Activo */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detalle por Activo</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Activo</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Precio Actual</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Valor Actual</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Invertido</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ganancia/Pérdida</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {holdings.map(h => (
                <tr key={h.ticker} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div
                        className="w-3 h-3 rounded-full mr-3"
                        style={{ backgroundColor: COLORS[h.ticker] }}
                      />
                      <span className="font-medium text-gray-900">{h.ticker}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                    {h.quantity.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                    ${h.currentPrice.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium text-gray-900">
                    ${h.currentValue.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                    ${h.invested.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <div className={h.gainLoss >= 0 ? 'text-green-600' : 'text-red-600'}>
                      <div className="font-medium">
                        {h.gainLoss >= 0 ? '+' : ''}${h.gainLoss.toFixed(2)}
                      </div>
                      <div className="text-xs">
                        ({h.gainLoss >= 0 ? '+' : ''}{h.gainLossPercent.toFixed(2)}%)
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default PortfolioDashboard
