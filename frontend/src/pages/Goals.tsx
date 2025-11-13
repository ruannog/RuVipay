import { useState, useMemo } from 'react'
import { useGoals, useDeleteGoal } from '../hooks/useApi'
import { Plus, Search, Target, Calendar, CheckCircle, AlertCircle, Trash2 } from 'lucide-react'
import GoalModal from '../components/GoalModal'

const Goals = () => {
  const [goalModalOpen, setGoalModalOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const { data: goalsResponse, isLoading, error } = useGoals()
  const deleteGoalMutation = useDeleteGoal()

  const goals = goalsResponse?.data || []

  // Filtrar metas baseado na pesquisa
  const filteredGoals = useMemo(() => {
    if (!searchTerm.trim()) return goals

    const searchLower = searchTerm.toLowerCase()
    return goals.filter((goal: any) => 
      goal.title.toLowerCase().includes(searchLower) ||
      goal.goal_type.toLowerCase().includes(searchLower) ||
      goal.period_type.toLowerCase().includes(searchLower)
    )
  }, [goals, searchTerm])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-100'
      case 'completed':
        return 'text-blue-600 bg-blue-100'
      case 'paused':
        return 'text-yellow-600 bg-yellow-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  const getProgressColor = (progress: number) => {
    if (progress >= 100) return 'bg-green-500'
    if (progress >= 75) return 'bg-blue-500'
    if (progress >= 50) return 'bg-yellow-500'
    if (progress >= 25) return 'bg-orange-500'
    return 'bg-red-500'
  }

  const getGoalTypeLabel = (type: string) => {
    const types: { [key: string]: string } = {
      'economia': 'Economia/Reserva',
      'investimento': 'Investimento',
      'compra': 'Compra',
      'viagem': 'Viagem',
      'outros': 'Outros'
    }
    return types[type] || type
  }

  const getPeriodTypeLabel = (type: string) => {
    const types: { [key: string]: string } = {
      'mensal': 'Mensal',
      'anual': 'Anual',
      'livre': 'Prazo Livre'
    }
    return types[type] || type
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(amount)
  }

  const getDaysRemaining = (endDate: string) => {
    const end = new Date(endDate)
    const now = new Date()
    const diffTime = end.getTime() - now.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays
  }

  const handleDeleteGoal = async (goalId: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta meta?')) {
      try {
        await deleteGoalMutation.mutateAsync(goalId)
        // A query será invalidada automaticamente pelo hook
      } catch (error) {
        console.error('Erro ao excluir meta:', error)
        alert('Erro ao excluir meta. Tente novamente.')
      }
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="mx-auto h-12 w-12 text-red-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">Erro ao carregar metas</h3>
        <p className="mt-1 text-sm text-gray-500">
          Não foi possível carregar suas metas. Tente novamente.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="md:flex md:items-center md:justify-between">
        <div className="min-w-0 flex-1">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
            Metas Financeiras
          </h2>
          <div className="mt-1 flex flex-col sm:mt-0 sm:flex-row sm:flex-wrap sm:space-x-6">
            <div className="mt-2 flex items-center text-sm text-gray-500">
              <Target className="mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400" />
              {goals.length} meta(s) cadastrada(s)
            </div>
          </div>
        </div>
        <div className="mt-4 flex md:ml-4 md:mt-0">
          <button
            type="button"
            onClick={() => setGoalModalOpen(true)}
            className="inline-flex items-center rounded-md bg-purple-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-purple-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-purple-600"
          >
            <Plus className="-ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
            Nova Meta
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
          <Search className="h-5 w-5 text-gray-400" aria-hidden="true" />
        </div>
        <input
          type="text"
          name="search"
          id="search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-purple-600 sm:text-sm sm:leading-6"
          placeholder="Pesquisar metas por título, tipo ou período..."
        />
      </div>

      {/* Goals Grid */}
      {filteredGoals.length === 0 ? (
        <div className="text-center py-12">
          <Target className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            {searchTerm ? 'Nenhuma meta encontrada' : 'Nenhuma meta cadastrada'}
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm 
              ? 'Tente ajustar os termos da pesquisa.' 
              : 'Comece criando sua primeira meta financeira.'
            }
          </p>
          {!searchTerm && (
            <div className="mt-6">
              <button
                type="button"
                onClick={() => setGoalModalOpen(true)}
                className="inline-flex items-center rounded-md bg-purple-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-purple-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-purple-600"
              >
                <Plus className="-ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
                Nova Meta
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filteredGoals.map((goal: any) => {
            const daysRemaining = getDaysRemaining(goal.end_date)
            const isCompleted = goal.progress_percentage >= 100
            const isExpired = daysRemaining < 0
            
            return (
              <div
                key={goal.id}
                className="relative overflow-hidden rounded-lg bg-white px-4 pb-12 pt-5 shadow sm:px-6 sm:pt-6 border border-gray-200 hover:shadow-md transition-shadow"
              >
                {/* Delete Button */}
                <div className="absolute top-4 left-4">
                  <button
                    onClick={() => handleDeleteGoal(goal.id)}
                    className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                    title="Excluir meta"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>

                {/* Status Badge */}
                <div className="absolute top-4 right-4">
                  <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${getStatusColor(goal.status)}`}>
                    {isCompleted ? (
                      <>
                        <CheckCircle className="mr-1 h-3 w-3" />
                        Concluída
                      </>
                    ) : isExpired ? (
                      <>
                        <AlertCircle className="mr-1 h-3 w-3" />
                        Vencida
                      </>
                    ) : (
                      goal.status
                    )}
                  </span>
                </div>

                {/* Goal Info */}
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 truncate pl-8 pr-20">
                    {goal.title}
                  </h3>
                  <p className="text-sm text-gray-500 mt-1">
                    {getGoalTypeLabel(goal.goal_type)} • {getPeriodTypeLabel(goal.period_type)}
                  </p>
                </div>

                {/* Progress */}
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">
                      Progresso
                    </span>
                    <span className="text-sm font-medium text-purple-600">
                      {goal.progress_percentage.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(goal.progress_percentage)}`}
                      style={{ width: `${Math.min(goal.progress_percentage, 100)}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>{formatCurrency(goal.current_amount)}</span>
                    <span>{formatCurrency(goal.target_amount)}</span>
                  </div>
                </div>

                {/* Dates */}
                <div className="flex items-center justify-between text-xs text-gray-500 mb-2">
                  <div className="flex items-center">
                    <Calendar className="mr-1 h-3 w-3" />
                    <span>{formatDate(goal.start_date)}</span>
                  </div>
                  <div className="flex items-center">
                    <span>até {formatDate(goal.end_date)}</span>
                  </div>
                </div>

                {/* Days Remaining */}
                <div className="text-center">
                  {isCompleted ? (
                    <span className="text-green-600 font-medium text-sm">
                      ✅ Meta atingida!
                    </span>
                  ) : isExpired ? (
                    <span className="text-red-600 font-medium text-sm">
                      ⏰ Vencida há {Math.abs(daysRemaining)} dias
                    </span>
                  ) : (
                    <span className="text-gray-600 text-sm">
                      {daysRemaining === 0 ? 'Vence hoje' : `${daysRemaining} dias restantes`}
                    </span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Goal Modal */}
      <GoalModal 
        isOpen={goalModalOpen} 
        onClose={() => setGoalModalOpen(false)}
      />
    </div>
  )
}

export default Goals