import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

// Configurar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptors para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Interfaces TypeScript
export interface Transaction {
  id: string
  description: string
  amount: number
  type: 'income' | 'expense'
  category?: string
  date: string
  status: 'completed' | 'pending'
}

export interface Category {
  id: string
  name: string
  type: 'income' | 'expense'
  color: string
  transactionCount: number
  totalAmount: number
}

export interface DashboardStats {
  totalIncome: number
  totalExpense: number
  balance: number
  transactionCount: number
  recentTransactions: Transaction[]
}

export interface ChartData {
  labels: string[]
  income: number[]
  expense: number[]
}

export interface UserProfile {
  id: string
  name: string
  email: string
  avatar: string
}

// API Methods
export const apiService = {
  // Transactions
  async getTransactions(): Promise<Transaction[]> {
    const response = await api.get('/transactions')
    return response.data.data
  },

  async getTransaction(id: string): Promise<Transaction> {
    const response = await api.get(`/transactions/${id}`)
    return response.data.data
  },

  async createTransaction(transaction: Omit<Transaction, 'id' | 'status'>): Promise<Transaction> {
    const response = await api.post('/transactions', transaction)
    return response.data.data
  },

  async updateTransaction(id: string, transaction: Partial<Transaction>): Promise<Transaction> {
    const response = await api.put(`/transactions/${id}`, transaction)
    return response.data.data
  },

  async deleteTransaction(id: string): Promise<void> {
    await api.delete(`/transactions/${id}`)
  },

  // Categories
  async getCategories(): Promise<Category[]> {
    const response = await api.get('/categories')
    return response.data.data
  },

  async createCategory(category: Omit<Category, 'id' | 'transactionCount' | 'totalAmount'>): Promise<Category> {
    const response = await api.post('/categories', category)
    return response.data.data
  },

  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await api.get('/dashboard/stats')
    return response.data.data
  },

  async getChartData(): Promise<ChartData> {
    const response = await api.get('/dashboard/chart-data')
    return response.data.data
  },

  // User
  async getUserProfile(): Promise<UserProfile> {
    const response = await api.get('/users/profile')
    return response.data.data
  },

  // Health check
  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await api.get('/test')
    return response.data
  }
}

export default apiService