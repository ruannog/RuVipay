import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiService } from '../services/api'
import type { Transaction, Category, DashboardStats, ChartData, UserProfile } from '../services/api'

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
    mutationFn: apiService.createTransaction,
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

export const useCreateCategory = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: apiService.createCategory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] })
    }
  })
}

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