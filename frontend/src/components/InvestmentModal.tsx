import React, { useState } from 'react'
import { X, TrendingUp } from 'lucide-react'

interface InvestmentModalProps {
  isOpen: boolean
  onClose: () => void
}

const InvestmentModal: React.FC<InvestmentModalProps> = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    name: '',
    investment_type: 'acao' as 'acao' | 'fundo' | 'cdi' | 'tesouro' | 'cripto' | 'outros',
    amount_invested: '',
    current_value: '',
    purchase_date: new Date().toISOString().split('T')[0]
  })

  const [isLoading, setIsLoading] = useState(false)

  const investmentTypes = [
    { value: 'acao', label: 'Ação' },
    { value: 'fundo', label: 'Fundo de Investimento' },
    { value: 'cdi', label: 'CDB/CDI' },
    { value: 'tesouro', label: 'Tesouro Direto' },
    { value: 'cripto', label: 'Criptomoeda' },
    { value: 'outros', label: 'Outros' }
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      // Aqui implementaremos a chamada para a API
      const investmentData = {
        name: formData.name,
        investment_type: formData.investment_type,
        amount_invested: parseFloat(formData.amount_invested),
        current_value: parseFloat(formData.current_value),
        purchase_date: formData.purchase_date
      }
      
      console.log('Criando investimento:', investmentData)
      
      // Reset form and close modal
      setFormData({
        name: '',
        investment_type: 'acao',
        amount_invested: '',
        current_value: '',
        purchase_date: new Date().toISOString().split('T')[0]
      })
      onClose()
    } catch (error) {
      console.error('Erro ao criar investimento:', error)
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

  // Auto-fill current_value with amount_invested if current_value is empty
  const handleAmountInvestedChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setFormData(prev => ({
      ...prev,
      amount_invested: value,
      current_value: prev.current_value || value
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
                <div className="flex items-center">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 sm:mx-0 sm:h-10 sm:w-10">
                    <TrendingUp className="h-6 w-6 text-indigo-600" />
                  </div>
                  <h3 className="ml-3 text-lg font-medium text-gray-900">
                    Novo Investimento
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

                {/* Investment Type */}
                <div>
                  <label htmlFor="investment_type" className="block text-sm font-medium text-gray-700">
                    Tipo de Investimento
                  </label>
                  <select
                    id="investment_type"
                    name="investment_type"
                    value={formData.investment_type}
                    onChange={handleInputChange}
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    {investmentTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Amount Invested */}
                <div>
                  <label htmlFor="amount_invested" className="block text-sm font-medium text-gray-700">
                    Valor Investido
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
                      onChange={handleAmountInvestedChange}
                      step="0.01"
                      min="0"
                      required
                      className="block w-full pl-10 border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="0,00"
                    />
                  </div>
                </div>

                {/* Current Value */}
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
                      className="block w-full pl-10 border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
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
                disabled={isLoading}
                className={`w-full inline-flex justify-center rounded-md border border-transparent px-4 py-2 text-base font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm bg-indigo-600 hover:bg-indigo-700 ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {isLoading ? 'Salvando...' : 'Salvar Investimento'}
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

export default InvestmentModal