import React, { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { useCreateInvestment, useUpdateInvestment } from '../hooks/useApi'

interface Investment {
  id: string
  name: string
  type: string
  amount_invested: number
  current_value: number
  purchase_date: string
  description?: string
}

interface InvestmentModalProps {
  isOpen: boolean
  onClose: () => void
  investment?: Investment | null
}

const InvestmentModal: React.FC<InvestmentModalProps> = ({ isOpen, onClose, investment }) => {
  const [formData, setFormData] = useState({
    name: '',
    type: 'Renda Fixa',
    amount_invested: '',
    current_value: '',
    purchase_date: new Date().toISOString().split('T')[0],
    description: ''
  })

  const createInvestmentMutation = useCreateInvestment()
  const updateInvestmentMutation = useUpdateInvestment()

  const isEditing = !!investment

  // Tipos de investimento disponíveis
  const investmentTypes = [
    'Renda Fixa',
    'Ações',
    'FII',
    'Cripto',
    'Commodities',
    'Outros'
  ]

  // Preencher formulário quando estiver editando
  useEffect(() => {
    if (investment) {
      setFormData({
        name: investment.name,
        type: investment.type,
        amount_invested: investment.amount_invested.toString(),
        current_value: investment.current_value.toString(),
        purchase_date: investment.purchase_date.split('T')[0], // Remove time part if exists
        description: investment.description || ''
      })
    } else {
      setFormData({
        name: '',
        type: 'Renda Fixa',
        amount_invested: '',
        current_value: '',
        purchase_date: new Date().toISOString().split('T')[0],
        description: ''
      })
    }
  }, [investment, isOpen])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      if (isEditing && investment) {
        await updateInvestmentMutation.mutateAsync({
          id: investment.id,
          investment: {
            name: formData.name,
            type: formData.type,
            amount_invested: parseFloat(formData.amount_invested),
            current_value: parseFloat(formData.current_value),
            purchase_date: formData.purchase_date,
            description: formData.description
          }
        })
        alert('Investimento atualizado com sucesso!')
      } else {
        const result = await createInvestmentMutation.mutateAsync({
          name: formData.name,
          type: formData.type,
          amount_invested: parseFloat(formData.amount_invested),
          current_value: parseFloat(formData.current_value),
          purchase_date: formData.purchase_date,
          description: formData.description
        })
        console.log('Investimento criado:', result)
        alert('Investimento criado com sucesso!')
      }
      
      // Reset form and close modal
      setFormData({
        name: '',
        type: 'Renda Fixa',
        amount_invested: '',
        current_value: '',
        purchase_date: new Date().toISOString().split('T')[0],
        description: ''
      })
      onClose()
    } catch (error) {
      console.error('Erro ao salvar investimento:', error)
      alert('Erro ao salvar investimento. Tente novamente.')
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
                  {isEditing ? 'Editar Investimento' : 'Novo Investimento'}
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
                {/* Investment Name */}
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                    Nome do Investimento
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Ex: ITUB4, Tesouro SELIC, Bitcoin..."
                  />
                </div>

                {/* Type */}
                <div>
                  <label htmlFor="type" className="block text-sm font-medium text-gray-700">
                    Tipo de Investimento
                  </label>
                  <select
                    id="type"
                    name="type"
                    value={formData.type}
                    onChange={handleInputChange}
                    required
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                  >
                    {investmentTypes.map(type => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Initial Amount */}
                <div>
                  <label htmlFor="amount_invested" className="block text-sm font-medium text-gray-700">
                    Valor Inicial Investido
                  </label>
                  <div className="mt-1 relative rounded-md shadow-sm">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">R$</span>
                    </div>
                    <input
                      type="number"
                      id="amount_invested"
                      name="amount_invested"
                      value={formData.amount_invested}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                      required
                      className="block w-full pl-10 border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      placeholder="0,00"
                    />
                  </div>
                </div>

                {/* Current Amount */}
                <div>
                  <label htmlFor="current_value" className="block text-sm font-medium text-gray-700">
                    Valor Atual
                  </label>
                  <div className="mt-1 relative rounded-md shadow-sm">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span className="text-gray-500 sm:text-sm">R$</span>
                    </div>
                    <input
                      type="number"
                      id="current_value"
                      name="current_value"
                      value={formData.current_value}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                      required
                      className="block w-full pl-10 border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      placeholder="0,00"
                    />
                  </div>
                </div>

                {/* Purchase Date */}
                <div>
                  <label htmlFor="purchase_date" className="block text-sm font-medium text-gray-700">
                    Data da Compra
                  </label>
                  <input
                    type="date"
                    id="purchase_date"
                    name="purchase_date"
                    value={formData.purchase_date}
                    onChange={handleInputChange}
                    required
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>

                {/* Description */}
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Descrição (Opcional)
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows={3}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                    placeholder="Adicione observações sobre este investimento..."
                  />
                </div>

                {/* Profit/Loss Indicator */}
                {formData.amount_invested && formData.current_value && (
                  <div className="bg-gray-50 p-3 rounded-md">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Resultado:</span>
                      <span className={`text-sm font-medium ${
                        parseFloat(formData.current_value) >= parseFloat(formData.amount_invested)
                          ? 'text-green-600'
                          : 'text-red-600'
                      }`}>
                        {parseFloat(formData.current_value) >= parseFloat(formData.amount_invested) ? '+' : ''}
                        {(parseFloat(formData.current_value) - parseFloat(formData.amount_invested)).toLocaleString('pt-BR', {
                          style: 'currency',
                          currency: 'BRL'
                        })}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="submit"
                disabled={createInvestmentMutation.isPending || updateInvestmentMutation.isPending}
                className={`w-full inline-flex justify-center rounded-md border border-transparent px-4 py-2 text-base font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm bg-green-600 hover:bg-green-700 ${
                  createInvestmentMutation.isPending || updateInvestmentMutation.isPending ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {createInvestmentMutation.isPending || updateInvestmentMutation.isPending 
                  ? 'Salvando...' 
                  : (isEditing ? 'Atualizar Investimento' : 'Salvar Investimento')
                }
              </button>
              <button
                type="button"
                onClick={onClose}
                className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
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

export default InvestmentModal