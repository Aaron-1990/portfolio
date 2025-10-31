/**
 * API Client
 * 
 * Cliente centralizado para comunicación con backend
 * 
 * Principios aplicados:
 * - Single Responsibility: Un cliente para todas las APIs
 * - Type Safety: TypeScript types para todas las respuestas
 * - Error Handling: Manejo centralizado de errores
 */

import axios, { AxiosInstance } from 'axios'

// Base URL del API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Crear instancia de axios
const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para logging (desarrollo)
axiosInstance.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejo de errores
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API Error]', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// API Methods
export const api = {
  // Portfolios
  portfolios: {
    list: async () => {
      const response = await axiosInstance.get('/portfolios')
      return response.data
    },
    
    get: async (id: number) => {
      const response = await axiosInstance.get(`/portfolios/${id}`)
      return response.data
    },
    
    create: async (data: any) => {
      const response = await axiosInstance.post('/portfolios', data)
      return response.data
    },
    
    update: async (id: number, data: any) => {
      const response = await axiosInstance.patch(`/portfolios/${id}`, data)
      return response.data
    },
    
    delete: async (id: number) => {
      const response = await axiosInstance.delete(`/portfolios/${id}`)
      return response.data
    },
    
    getSummary: async (id: number) => {
      const response = await axiosInstance.get(`/portfolios/${id}/summary`)
      return response.data
    },
  },

  // Prices
  prices: {
    getLatest: async (tickers?: string[]) => {
      const params = tickers ? { tickers: tickers.join(',') } : {}
      const response = await axiosInstance.get('/prices/latest', { params })
      return response.data
    },
    
    refresh: async (tickers?: string[]) => {
      const params = tickers ? { tickers: tickers.join(',') } : {}
      const response = await axiosInstance.post('/prices/refresh', null, { params })
      return response.data
    },
    
    getHistory: async (ticker: string, days: number = 30) => {
      const response = await axiosInstance.get(`/prices/history/${ticker}`, {
        params: { days },
      })
      return response.data
    },
  },

  // Holdings
  holdings: {
    list: async (portfolioId: number) => {
      const response = await axiosInstance.get('/holdings', {
        params: { portfolio_id: portfolioId },
      })
      return response.data
    },
    
    create: async (data: any) => {
      const response = await axiosInstance.post('/holdings', data)
      return response.data
    },
  },

  // Transactions
  transactions: {
    list: async (portfolioId: number) => {
      const response = await axiosInstance.get('/transactions', {
        params: { portfolio_id: portfolioId },
      })
      return response.data
    },
    
    create: async (data: any) => {
      const response = await axiosInstance.post('/transactions', data)
      return response.data
    },
  },
}

export default axiosInstance
