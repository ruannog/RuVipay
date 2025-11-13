import React, { useState } from 'react'
import { X, Target, CheckCircle } from 'lucide-react'
import { useCategories, useCreateGoal } from '../hooks/useApi'

interface GoalModalProps {
  isOpen: boolean
  onClose: () => void
}

const GoalModal: React.FC<GoalModalProps> = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    title: '',
    goal_type: 'economia' as 'economia' | 'investimento' | 'compra' | 'viagem' | 'outros',
    target_amount: '',
    current_amount: '0',
    period_type: 'mensal' as 'mensal' | 'anual' | 'livre',
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    category_id: ''
  })

  const [isLoading, setIsLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const { data: categories = [] } = useCategories()
  const createGoalMutation = useCreateGoal()

  const goalTypes = [
    { value: 'economia', label: 'Economia/Reserva' },
    { value: 'investimento', label: 'Investimento' },
    { value: 'compra', label: 'Compra' },
    { value: 'viagem', label: 'Viagem' },
    { value: 'outros', label: 'Outros' }
  ]

  const periodTypes = [
    { value: 'mensal', label: 'Mensal' },
    { value: 'anual', label: 'Anual' },
    { value: 'livre', label: 'Prazo Livre' }
  ]

  // Calculate suggested end date based on period type
  const calculateEndDate = (startDate: string, period: string) => {
    const start = new Date(startDate)
    if (period === 'mensal') {
      start.setMonth(start.getMonth() + 1)
    } else if (period === 'anual') {
      start.setFullYear(start.getFullYear() + 1)
    } else {
      start.setMonth(start.getMonth() + 6) // Default 6 months for free period
    }
    return start.toISOString().split('T')[0]
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      // Usar a mutation para criar a meta
      await createGoalMutation.mutateAsync({
        title: formData.title,
        goal_type: formData.goal_type,
        target_amount: parseFloat(formData.target_amount),
        current_amount: parseFloat(formData.current_amount),
        period_type: formData.period_type,
        start_date: formData.start_date,
        end_date: formData.end_date,
        category_id: formData.category_id ? parseInt(formData.category_id) : undefined
      })
      
      // Mostrar mensagem de sucesso
      setSuccessMessage('Meta criada com sucesso!')
      
      // Aguardar um pouco antes de fechar o modal para mostrar a mensagem
      setTimeout(() => {
        setSuccessMessage('')
        // Reset form and close modal
        setFormData({
          title: '',
          goal_type: 'economia',
          target_amount: '',
          current_amount: '0',
          period_type: 'mensal',
          start_date: new Date().toISOString().split('T')[0],
          end_date: '',
          category_id: ''
        })
        onClose()
      }, 1500)
    } catch (error) {
      console.error('Erro ao criar meta:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handlePeriodChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const period = e.target.value
    setFormData(prev => ({
      ...prev,
      period_type: period as any,
      end_date: calculateEndDate(prev.start_date, period)
    }))
  }

  const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const startDate = e.target.value
    setFormData(prev => ({
      ...prev,
      start_date: startDate,
      end_date: calculateEndDate(startDate, prev.period_type)
    }))
  }

  const progressPercentage = formData.target_amount && formData.current_amount
    ? Math.min((parseFloat(formData.current_amount) / parseFloat(formData.target_amount)) * 100, 100)
    : 0

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div 
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          onClick={onClose}
        />

        {/* Modal */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form onSubmit={handleSubmit}>
            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-purple-100 sm:mx-0 sm:h-10 sm:w-10">
                    <Target className="h-6 w-6 text-purple-600" />
                  </div>
                  <h3 className="ml-3 text-lg font-medium text-gray-900">
                    Nova Meta
                  </h3>
                </div>
                <button
                  type="button"
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              {/* Success Message */}
              {successMessage && (
                <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-md">
                  <div className="flex">
                    <CheckCircle className="h-5 w-5 text-green-400" />
                    <div className="ml-3">
                      <p className="text-sm text-green-700">{successMessage}</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="space-y-4">
                {/* Goal Title */}
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                    Título da Meta
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    required
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    placeholder="Ex: Reserva de Emergência, Viagem para Europa..."
                  />
                </div>

                {/* Goal Type */}
                <div>
                  <label htmlFor="goal_type" className="block text-sm font-medium text-gray-700">
                    Tipo da Meta
                  </label>
                  <select
                    id="goal_type"
                    name="goal_type"
                    value={formData.goal_type}
                    onChange={handleInputChange}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  >
                    {goalTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Target Amount */}
                <div>
                  <label htmlFor="target_amount" className="block text-sm font-medium text-gray-700">
                    Valor da Meta
                  </label>
                  <div className="mt-1 relative rounded-md shadow-sm">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">R$</span>
                    </div>
                    <input
                      type="number"
                      id="target_amount"
                      name="target_amount"
                      value={formData.target_amount}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                      required
                      className="block w-full pl-10 border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                      placeholder="0,00"
                    />
                  </div>
                </div>

                {/* Current Amount */}
                <div>
                  <label htmlFor="current_amount" className="block text-sm font-medium text-gray-700">
                    Valor Atual
                  </label>
                  <div className="mt-1 relative rounded-md shadow-sm">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">R$</span>
                    </div>
                    <input
                      type="number"
                      id="current_amount"
                      name="current_amount"
                      value={formData.current_amount}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                      className="block w-full pl-10 border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                      placeholder="0,00"
                    />
                  </div>
                </div>

                {/* Period Type */}
                <div>
                  <label htmlFor="period_type" className="block text-sm font-medium text-gray-700">
                    Período
                  </label>
                  <select
                    id="period_type"
                    name="period_type"
                    value={formData.period_type}
                    onChange={handlePeriodChange}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  >
                    {periodTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Date Range */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="start_date" className="block text-sm font-medium text-gray-700">
                      Data Início
                    </label>
                    <input
                      type="date"
                      id="start_date"
                      name="start_date"
                      value={formData.start_date}
                      onChange={handleStartDateChange}
                      required
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    />
                  </div>
                  <div>
                    <label htmlFor="end_date" className="block text-sm font-medium text-gray-700">
                      Data Meta
                    </label>
                    <input
                      type="date"
                      id="end_date"
                      name="end_date"
                      value={formData.end_date}
                      onChange={handleInputChange}
                      required
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                    />
                  </div>
                </div>

                {/* Category */}
                <div>
                  <label htmlFor="category_id" className="block text-sm font-medium text-gray-700">
                    Categoria (Opcional)
                  </label>
                  <select
                    id="category_id"
                    name="category_id"
                    value={formData.category_id}
                    onChange={handleInputChange}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500"
                  >
                    <option value="">Selecione uma categoria</option>
                    {categories.map(category => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Progress Indicator */}
                {formData.target_amount && (
                  <div className="bg-gray-50 p-3 rounded-md">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-600">Progresso:</span>
                      <span className="text-sm font-medium text-purple-600">
                        {progressPercentage.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${progressPercentage}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>R$ {parseFloat(formData.current_amount || '0').toLocaleString('pt-BR')}</span>
                      <span>R$ {parseFloat(formData.target_amount).toLocaleString('pt-BR')}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="submit"
                disabled={isLoading}
                className={`w-full inline-flex justify-center rounded-md border border-transparent px-4 py-2 text-base font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:ml-3 sm:w-auto sm:text-sm bg-purple-600 hover:bg-purple-700 ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {isLoading ? 'Salvando...' : 'Criar Meta'}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default GoalModal