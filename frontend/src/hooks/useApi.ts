import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiService } from '../services/api'
import type { Transaction, Investment, Goal } from '../services/api'

// Dashboard Hooks
export const useDashboardStats = () => {
  return useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: apiService.getDashboardStats,
    staleTime: 5 * 60 * 1000, // 5 minutos
    retry: 2
  })
}

export const useChartData = (period: string) => {
  return useQuery({
    queryKey: ['chart-data', period],
    queryFn: apiService.getChartData,
    staleTime: 10 * 60 * 1000, // 10 minutos
    retry: 2
  })
}

// Transaction Hooks
export const useTransactions = () => {
  return useQuery({
    queryKey: ['transactions'],
    queryFn: apiService.getTransactions,
    staleTime: 2 * 60 * 1000, // 2 minutos
    retry: 2
  })
}

export const useSearchTransactions = (searchParams: {
  q?: string;
  start_date?: string;
  end_date?: string;
  category?: string;
  type?: string;
}) => {
  return useQuery({
    queryKey: ['transactions', 'search', searchParams],
    queryFn: () => apiService.searchTransactions(searchParams),
    enabled: Object.values(searchParams).some(value => value !== undefined && value !== ''),
    staleTime: 1 * 60 * 1000, // 1 minuto
    retry: 2
  })
}

export const useTransaction = (id: string) => {
  return useQuery({
    queryKey: ['transaction', id],
    queryFn: () => apiService.getTransaction(id),
    enabled: !!id,
    retry: 2
  })
}

export const useCreateTransaction = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (transaction: Omit<Transaction, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => 
      apiService.createTransaction(transaction),
    onSuccess: () => {
      // Invalidar queries relacionadas para refetch automático
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      queryClient.invalidateQueries({ queryKey: ['chart-data'] })
    },
    onError: (error) => {
      console.error('Erro ao criar transação:', error)
    }
  })
}

export const useUpdateTransaction = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, transaction }: { id: string; transaction: Partial<Transaction> }) =>
      apiService.updateTransaction(id, transaction),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
    }
  })
}

export const useDeleteTransaction = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: apiService.deleteTransaction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
    }
  })
}

// Category Hooks
export const useCategories = () => {
  return useQuery({
    queryKey: ['categories'],
    queryFn: apiService.getCategories,
    staleTime: 15 * 60 * 1000, // 15 minutos
    retry: 2
  })
}
// Note: category create/delete hooks removed because Categories page was removed.

// User Hooks
export const useUserProfile = () => {
  return useQuery({
    queryKey: ['user-profile'],
    queryFn: apiService.getUserProfile,
    staleTime: 30 * 60 * 1000, // 30 minutos
    retry: 2
  })
}

// Health Check Hook
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health-check'],
    queryFn: apiService.healthCheck,
    refetchInterval: 30 * 1000, // Verificar a cada 30 segundos
    retry: 1,
    retryDelay: 1000
  })
}

// Investment Hooks
export const useInvestments = () => {
  return useQuery({
    queryKey: ['investments'],
    queryFn: apiService.getInvestments,
    staleTime: 30 * 1000, // 30 segundos
    retry: 2
  })
}

export const useInvestment = (id: string) => {
  return useQuery({
    queryKey: ['investment', id],
    queryFn: () => apiService.getInvestment(id),
    enabled: !!id,
    retry: 2
  })
}

export const useCreateInvestment = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (investment: Omit<Investment, 'id' | 'user_id' | 'created_at' | 'updated_at' | 'profit_loss' | 'profit_loss_percentage'>) => 
      apiService.createInvestment(investment),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investments'] })
      queryClient.invalidateQueries({ queryKey: ['investment-stats'] })
    },
    onError: (error) => {
      console.error('Erro ao criar investimento:', error)
    }
  })
}

export const useUpdateInvestment = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, investment }: { id: string; investment: Partial<Investment> }) =>
      apiService.updateInvestment(id, investment),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investments'] })
      queryClient.invalidateQueries({ queryKey: ['investment-stats'] })
    }
  })
}

export const useDeleteInvestment = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: apiService.deleteInvestment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investments'] })
      queryClient.invalidateQueries({ queryKey: ['investment-stats'] })
    }
  })
}

export const useInvestmentStats = () => {
  return useQuery({
    queryKey: ['investment-stats'],
    queryFn: apiService.getInvestmentStats,
    staleTime: 5 * 60 * 1000, // 5 minutos
    retry: 2
  })
}

// Goal Hooks
export const useGoals = () => {
  return useQuery({
    queryKey: ['goals'],
    queryFn: apiService.getGoals,
    staleTime: 30 * 1000, // 30 segundos
    retry: 2
  })
}

export const useGoal = (id: string) => {
  return useQuery({
    queryKey: ['goal', id],
    queryFn: () => apiService.getGoal(id),
    enabled: !!id,
    retry: 2
  })
}

export const useCreateGoal = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (goal: Omit<Goal, 'id' | 'status' | 'progress_percentage'>) => 
      apiService.createGoal(goal),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] })
      queryClient.invalidateQueries({ queryKey: ['goal-stats'] })
    },
    onError: (error) => {
      console.error('Erro ao criar meta:', error)
    }
  })
}

export const useUpdateGoal = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, goal }: { id: string; goal: Partial<Goal> }) =>
      apiService.updateGoal(id, goal),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] })
      queryClient.invalidateQueries({ queryKey: ['goal-stats'] })
    }
  })
}

export const useDeleteGoal = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: apiService.deleteGoal,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] })
      queryClient.invalidateQueries({ queryKey: ['goal-stats'] })
    }
  })
}

export const useGoalStats = () => {
  return useQuery({
    queryKey: ['goal-stats'],
    queryFn: apiService.getGoalStats,
    staleTime: 5 * 60 * 1000, // 5 minutos
    retry: 2
  })
}