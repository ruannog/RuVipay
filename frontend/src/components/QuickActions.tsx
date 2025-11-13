import { Plus, Minus, TrendingUp, Target } from 'lucide-react'
import { useState } from 'react'
import TransactionModal from './TransactionModal'
import InvestmentModal from './InvestmentModal'
import GoalModal from './GoalModal'

const QuickActions = () => {
  const [transactionModalOpen, setTransactionModalOpen] = useState(false)
  const [transactionType, setTransactionType] = useState<'income' | 'expense'>('income')
  const [investmentModalOpen, setInvestmentModalOpen] = useState(false)
  const [goalModalOpen, setGoalModalOpen] = useState(false)

  const openTransactionModal = (type: 'income' | 'expense') => {
    setTransactionType(type)
    setTransactionModalOpen(true)
  }

  const actions = [
    {
      name: 'Nova Receita',
      description: 'Adicionar receita',
      icon: Plus,
      color: 'bg-green-500 hover:bg-green-600',
      onClick: () => openTransactionModal('income')
    },
    {
      name: 'Nova Despesa',
      description: 'Adicionar despesa',
      icon: Minus,
      color: 'bg-red-500 hover:bg-red-600',
      onClick: () => openTransactionModal('expense')
    },
    {
      name: 'Meta',
      description: 'Definir meta',
      icon: Target,
      color: 'bg-purple-500 hover:bg-purple-600',
      onClick: () => setGoalModalOpen(true)
    },
    {
      name: 'Investimento',
      description: 'Registrar investimento',
      icon: TrendingUp,
      color: 'bg-indigo-500 hover:bg-indigo-600',
      onClick: () => setInvestmentModalOpen(true)
    },
  ]

  return (
    <>
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Ações Rápidas
        </h3>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {actions.map((action) => (
            <button
              key={action.name}
              onClick={action.onClick}
              className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors group"
            >
              <div className={`p-3 rounded-full ${action.color} transition-colors`}>
                <action.icon className="h-6 w-6 text-white" />
              </div>
              <span className="mt-2 text-sm font-medium text-gray-900">
                {action.name}
              </span>
              <span className="text-xs text-gray-500 text-center">
                {action.description}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Modals */}
      <TransactionModal 
        isOpen={transactionModalOpen} 
        onClose={() => setTransactionModalOpen(false)}
      />
      <InvestmentModal 
        isOpen={investmentModalOpen} 
        onClose={() => setInvestmentModalOpen(false)}
      />
      <GoalModal 
        isOpen={goalModalOpen} 
        onClose={() => setGoalModalOpen(false)}
      />
    </>
  )
}

export default QuickActions