import { useState } from 'react'
import { Plus, Edit, Trash2, MoreHorizontal, Tag } from 'lucide-react'

interface Category {
  id: string
  name: string
  type: 'income' | 'expense'
  color: string
  transactionCount: number
  totalAmount: number
}

const Categories = () => {
  const [activeTab, setActiveTab] = useState<'income' | 'expense'>('expense')
  const [showModal, setShowModal] = useState(false)

  // Mock data - substituir por dados reais da API
  const categories: Category[] = [
    {
      id: '1',
      name: 'Alimentação',
      type: 'expense',
      color: '#ef4444',
      transactionCount: 15,
      totalAmount: 890.50
    },
    {
      id: '2',
      name: 'Transporte',
      type: 'expense',
      color: '#f97316',
      transactionCount: 8,
      totalAmount: 420.00
    },
    {
      id: '3',
      name: 'Saúde',
      type: 'expense',
      color: '#06b6d4',
      transactionCount: 3,
      totalAmount: 280.00
    },
    {
      id: '4',
      name: 'Lazer',
      type: 'expense',
      color: '#8b5cf6',
      transactionCount: 6,
      totalAmount: 350.00
    },
    {
      id: '5',
      name: 'Salário',
      type: 'income',
      color: '#10b981',
      transactionCount: 1,
      totalAmount: 3500.00
    },
    {
      id: '6',
      name: 'Freelance',
      type: 'income',
      color: '#06b6d4',
      transactionCount: 2,
      totalAmount: 1800.00
    },
    {
      id: '7',
      name: 'Investimentos',
      type: 'income',
      color: '#8b5cf6',
      transactionCount: 4,
      totalAmount: 245.30
    }
  ]

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(amount)
  }

  const filteredCategories = categories.filter(category => category.type === activeTab)

  const totalAmount = filteredCategories.reduce((sum, category) => sum + category.totalAmount, 0)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Categorias</h1>
        <button 
          onClick={() => setShowModal(true)}
          className="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500"
        >
          <Plus className="h-4 w-4 mr-1" />
          Nova Categoria
        </button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('expense')}
            className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'expense'
                ? 'border-red-500 text-red-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Despesas
          </button>
          <button
            onClick={() => setActiveTab('income')}
            className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'income'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Receitas
          </button>
        </nav>
      </div>

      {/* Summary Card */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Tag className={`h-6 w-6 ${activeTab === 'income' ? 'text-green-400' : 'text-red-400'}`} />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Total {activeTab === 'income' ? 'Receitas' : 'Despesas'}
                </dt>
                <dd className={`text-lg font-medium ${activeTab === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                  {formatCurrency(totalAmount)}
                </dd>
              </dl>
            </div>
            <div className="ml-5 text-sm text-gray-500">
              {filteredCategories.length} categorias
            </div>
          </div>
        </div>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filteredCategories.map((category) => (
          <div key={category.id} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div 
                    className="h-8 w-8 rounded-full flex items-center justify-center"
                    style={{ backgroundColor: category.color }}
                  >
                    <Tag className="h-4 w-4 text-white" />
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-900 truncate">
                      {category.name}
                    </dt>
                    <dd className={`text-lg font-medium ${
                      category.type === 'income' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {formatCurrency(category.totalAmount)}
                    </dd>
                  </dl>
                </div>
                <div className="ml-5">
                  <button className="text-gray-400 hover:text-gray-600">
                    <MoreHorizontal className="h-5 w-5" />
                  </button>
                </div>
              </div>
              
              <div className="mt-4">
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>{category.transactionCount} transações</span>
                  <div className="flex space-x-2">
                    <button className="text-blue-600 hover:text-blue-800">
                      <Edit className="h-4 w-4" />
                    </button>
                    <button className="text-red-600 hover:text-red-800">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
                
                <div className="mt-2 bg-gray-200 rounded-full h-2">
                  <div
                    className="h-2 rounded-full"
                    style={{ 
                      backgroundColor: category.color,
                      width: `${(category.totalAmount / totalAmount) * 100}%`
                    }}
                  />
                </div>
                
                <div className="mt-1 text-xs text-gray-500">
                  {((category.totalAmount / totalAmount) * 100).toFixed(1)}% do total
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredCategories.length === 0 && (
        <div className="text-center py-12">
          <Tag className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            Nenhuma categoria encontrada
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            Comece criando uma nova categoria.
          </p>
          <div className="mt-6">
            <button
              onClick={() => setShowModal(true)}
              className="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500"
            >
              <Plus className="h-4 w-4 mr-1" />
              Nova Categoria
            </button>
          </div>
        </div>
      )}

      {/* Modal para nova categoria (implementar depois) */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <h3 className="text-lg font-medium text-gray-900">Nova Categoria</h3>
              <div className="mt-2 px-7 py-3">
                <p className="text-sm text-gray-500">
                  Modal para criar nova categoria (implementar formulário)
                </p>
              </div>
              <div className="items-center px-4 py-3">
                <button
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-600"
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Categories