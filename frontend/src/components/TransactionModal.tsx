import React, { useState, useEffect } from 'react'
import { X, Plus, Minus } from 'lucide-react'
import { useCreateTransaction, useUpdateTransaction } from '../hooks/useApi'

interface Transaction {
  id: string
  description: string
  amount: number
  type: 'income' | 'expense'
  category?: string
  date: string
  status?: 'completed' | 'pending'
}

interface TransactionModalProps {
  isOpen: boolean
  onClose: () => void
  transaction?: Transaction | null
}

const TransactionModal: React.FC<TransactionModalProps> = ({ isOpen, onClose, transaction }) => {
  const [formData, setFormData] = useState({
    description: '',
    amount: '',
    type: 'income' as 'income' | 'expense',
    category: '',
    date: new Date().toISOString().split('T')[0]
  })

  const createTransactionMutation = useCreateTransaction()
  const updateTransactionMutation = useUpdateTransaction()

  const isEditing = !!transaction

  // Preencher formulário quando estiver editando
  useEffect(() => {
    if (transaction) {
      setFormData({
        description: transaction.description,
        amount: transaction.amount.toString(),
        type: transaction.type,
        category: transaction.category || '',
        date: transaction.date.split('T')[0] // Remove time part if exists
      })
    } else {
      setFormData({
        description: '',
        amount: '',
        type: 'income',
        category: '',
        date: new Date().toISOString().split('T')[0]
      })
    }
  }, [transaction, isOpen])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      if (isEditing && transaction) {
        await updateTransactionMutation.mutateAsync({
          id: transaction.id,
          transaction: {
            description: formData.description,
            amount: parseFloat(formData.amount),
            type: formData.type,
            category: formData.category,
            date: formData.date
          }
        })
      } else {
        await createTransactionMutation.mutateAsync({
          description: formData.description,
          amount: parseFloat(formData.amount),
          type: formData.type,
          category: formData.category,
          date: formData.date
        })
      }
      
      // Reset form and close modal
      setFormData({
        description: '',
        amount: '',
        type: 'income',
        category: '',
        date: new Date().toISOString().split('T')[0]
      })
      onClose()
    } catch (error) {
      console.error('Erro ao salvar transação:', error)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

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
                <h3 className="text-lg font-medium text-gray-900">
                  {isEditing ? 'Editar Transação' : 'Nova Transação'}
                </h3>
                <button
                  type="button"
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              <div className="space-y-4">
                {/* Transaction Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tipo da Transação
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, type: 'income', category: '' }))}
                      className={`flex items-center justify-center px-3 py-2 border rounded-md ${
                        formData.type === 'income'
                          ? 'border-green-500 bg-green-50 text-green-700'
                          : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Receita
                    </button>
                    <button
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, type: 'expense', category: '' }))}
                      className={`flex items-center justify-center px-3 py-2 border rounded-md ${
                        formData.type === 'expense'
                          ? 'border-red-500 bg-red-50 text-red-700'
                          : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Minus className="h-4 w-4 mr-2" />
                      Despesa
                    </button>
                  </div>
                </div>

                {/* Description */}
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Descrição
                  </label>
                  <input
                    type="text"
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    required
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Ex: Salário, Supermercado, etc..."
                  />
                </div>

                {/* Amount */}
                <div>
                  <label htmlFor="amount" className="block text-sm font-medium text-gray-700">
                    Valor
                  </label>
                  <div className="mt-1 relative rounded-md shadow-sm">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">R$</span>
                    </div>
                    <input
                      type="number"
                      id="amount"
                      name="amount"
                      value={formData.amount}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                      required
                      className="block w-full pl-10 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                      placeholder="0,00"
                    />
                  </div>
                </div>

                {/* Category */}
                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-gray-700">
                    Categoria
                  </label>
                  <select
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    required
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Selecione uma categoria</option>
                    {formData.type === 'income' ? (
                      <>
                        <option value="Salário">Salário</option>
                        <option value="Trabalho Extra">Trabalho Extra</option>
                        <option value="Investimentos">Investimentos</option>
                        <option value="Vendas">Vendas</option>
                      </>
                    ) : (
                      <>
                        <option value="Alimentação">Alimentação</option>
                        <option value="Transporte">Transporte</option>
                        <option value="Saúde">Saúde</option>
                        <option value="Lazer">Lazer</option>
                        <option value="Utilidades">Utilidades</option>
                        <option value="Compras">Compras</option>
                      </>
                    )}
                  </select>
                </div>

                {/* Date */}
                <div>
                  <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                    Data
                  </label>
                  <input
                    type="date"
                    id="date"
                    name="date"
                    value={formData.date}
                    onChange={handleInputChange}
                    required
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="submit"
                disabled={createTransactionMutation.isPending || updateTransactionMutation.isPending}
                className={`w-full inline-flex justify-center rounded-md border border-transparent px-4 py-2 text-base font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm ${
                  formData.type === 'income'
                    ? 'bg-green-600 hover:bg-green-700 focus:ring-green-500'
                    : 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
                } ${createTransactionMutation.isPending || updateTransactionMutation.isPending ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {createTransactionMutation.isPending || updateTransactionMutation.isPending ? 
                  'Salvando...' : 
                  isEditing ? 'Atualizar' : 'Salvar'
                }
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

export default TransactionModal