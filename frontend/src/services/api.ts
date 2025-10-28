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
    try {
      const response = await api.get('/transactions')
      // O backend retorna { status: "success", data: [...] }
      return response.data.data || response.data || []
    } catch (error) {
      console.error('Erro ao buscar transações:', error)
      return []
    }
  },

  async searchTransactions(params: {
    q?: string;
    start_date?: string;
    end_date?: string;
    category?: string;
    type?: string;
  }): Promise<Transaction[]> {
    try {
      const searchParams = new URLSearchParams()
      if (params.q) searchParams.append('q', params.q)
      if (params.start_date) searchParams.append('start_date', params.start_date)
      if (params.end_date) searchParams.append('end_date', params.end_date)
      if (params.category) searchParams.append('category', params.category)
      if (params.type) searchParams.append('type', params.type)
      
      const response = await api.get(`/transactions/search?${searchParams.toString()}`)
      return response.data.data || response.data || []
    } catch (error) {
      console.error('Erro ao buscar transações:', error)
      return []
    }
  },

  async getTransaction(id: string): Promise<Transaction> {
    try {
      const response = await api.get(`/transactions/${id}`)
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao buscar transação:', error)
      throw error
    }
  },

  async createTransaction(transaction: Omit<Transaction, 'id' | 'status'>): Promise<Transaction> {
    try {
      const response = await api.post('/transactions', transaction)
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao criar transação:', error)
      throw error
    }
  },

  async updateTransaction(id: string, transaction: Partial<Transaction>): Promise<Transaction> {
    try {
      const response = await api.put(`/transactions/${id}`, transaction)
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao atualizar transação:', error)
      throw error
    }
  },

  async deleteTransaction(id: string): Promise<void> {
    try {
      await api.delete(`/transactions/${id}`)
    } catch (error) {
      console.error('Erro ao deletar transação:', error)
      throw error
    }
  },

  // Categories
  async getCategories(): Promise<Category[]> {
    try {
      const response = await api.get('/categories')
      return response.data.data || response.data || []
    } catch (error) {
      console.error('Erro ao buscar categorias:', error)
      return []
    }
  },

  async createCategory(category: Omit<Category, 'id' | 'transactionCount' | 'totalAmount'>): Promise<Category> {
    try {
      const response = await api.post('/categories', category)
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao criar categoria:', error)
      throw error
    }
  },

  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    try {
      const response = await api.get('/dashboard/stats')
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
      throw error
    }
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