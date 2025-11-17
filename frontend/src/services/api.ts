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
  category_id: number
  date: string
  notes?: string
  user_id?: number
  created_at?: string
  updated_at?: string
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

export interface Investment {
  id: string
  name: string
  type: string
  amount_invested: number
  current_value: number
  purchase_date: string
  description?: string
  user_id: number
  created_at?: string
  updated_at?: string
  profit_loss?: number
  profit_loss_percentage?: number
}

export interface InvestmentStats {
  total_invested: number
  total_current: number
  profit_loss: number
  profit_percentage: number
  investment_count: number
  best_investment: {
    name: string | null
    profit_percentage: number
  }
}

export interface Goal {
  id: string
  title: string
  goal_type: 'economia' | 'investimento' | 'compra' | 'viagem' | 'outros'
  target_amount: number
  current_amount: number
  period_type: 'mensal' | 'anual' | 'livre'
  start_date: string
  end_date: string
  category_id?: number
  status: 'active' | 'completed' | 'paused'
  progress_percentage: number
}

export interface GoalStats {
  total_goals: number
  completed_goals: number
  total_target_amount: number
  total_current_amount: number
  average_progress: number
  best_goal: {
    title: string | null
    progress: number
  }
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

  async createTransaction(transaction: Omit<Transaction, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<Transaction> {
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
  // create/delete category methods intentionally removed because Categories page was removed

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
  },

  // Investments
  async getInvestments(): Promise<Investment[]> {
    try {
      const response = await api.get('/investments')
      return response.data.data || response.data || []
    } catch (error) {
      console.error('Erro ao buscar investimentos:', error)
      return []
    }
  },

  async getInvestment(id: string): Promise<Investment> {
    try {
      const response = await api.get(`/investments/${id}`)
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao buscar investimento:', error)
      throw error
    }
  },

  async createInvestment(investment: Omit<Investment, 'id' | 'user_id' | 'created_at' | 'updated_at' | 'profit_loss' | 'profit_loss_percentage'>): Promise<Investment> {
    try {
      const response = await api.post('/investments', investment)
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao criar investimento:', error)
      throw error
    }
  },

  async updateInvestment(id: string, investment: Partial<Investment>): Promise<Investment> {
    try {
      const response = await api.put(`/investments/${id}`, investment)
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao atualizar investimento:', error)
      throw error
    }
  },

  async deleteInvestment(id: string): Promise<void> {
    try {
      await api.delete(`/investments/${id}`)
    } catch (error) {
      console.error('Erro ao deletar investimento:', error)
      throw error
    }
  },

  async getInvestmentStats(): Promise<InvestmentStats> {
    try {
      const response = await api.get('/investments/stats')
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao buscar estatísticas de investimentos:', error)
      throw error
    }
  },

  // Goals
  async getGoals(): Promise<{ data: Goal[] }> {
    try {
      const response = await api.get('/goals/')
      // O backend retorna lista direta, não { data: [] }
      return { data: response.data }
    } catch (error) {
      console.error('Erro ao buscar metas:', error)
      throw error
    }
  },

  async getGoal(id: string): Promise<Goal> {
    try {
      const response = await api.get(`/goals/${id}`)
      return response.data
    } catch (error) {
      console.error('Erro ao buscar meta:', error)
      throw error
    }
  },

  async createGoal(goal: Omit<Goal, 'id' | 'status' | 'progress_percentage'>): Promise<Goal> {
    try {
      const response = await api.post('/goals/', goal)
      // O backend retorna o objeto diretamente, não { data: {} }
      return response.data
    } catch (error) {
      console.error('Erro ao criar meta:', error)
      throw error
    }
  },

  async updateGoal(id: string, goal: Partial<Goal>): Promise<Goal> {
    try {
      const response = await api.put(`/goals/${id}`, goal)
      return response.data
    } catch (error) {
      console.error('Erro ao atualizar meta:', error)
      throw error
    }
  },

  async deleteGoal(id: string): Promise<void> {
    try {
      await api.delete(`/goals/${id}`)
    } catch (error) {
      console.error('Erro ao deletar meta:', error)
      throw error
    }
  },

  async getGoalStats(): Promise<GoalStats> {
    try {
      const response = await api.get('/goals/stats')
      return response.data.data || response.data
    } catch (error) {
      console.error('Erro ao buscar estatísticas de metas:', error)
      throw error
    }
  }
}

export default apiService