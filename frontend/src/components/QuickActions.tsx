import { Plus, Minus, TrendingUp, FileText, Target, CreditCard } from 'lucide-react'

const QuickActions = () => {
  const actions = [
    {
      name: 'Nova Receita',
      description: 'Adicionar receita',
      icon: Plus,
      color: 'bg-green-500 hover:bg-green-600',
      onClick: () => console.log('Nova receita')
    },
    {
      name: 'Nova Despesa',
      description: 'Adicionar despesa',
      icon: Minus,
      color: 'bg-red-500 hover:bg-red-600',
      onClick: () => console.log('Nova despesa')
    },
    {
      name: 'Relatório',
      description: 'Gerar relatório',
      icon: FileText,
      color: 'bg-blue-500 hover:bg-blue-600',
      onClick: () => console.log('Relatório')
    },
    {
      name: 'Meta',
      description: 'Definir meta',
      icon: Target,
      color: 'bg-purple-500 hover:bg-purple-600',
      onClick: () => console.log('Meta')
    },
    {
      name: 'Investimento',
      description: 'Registrar investimento',
      icon: TrendingUp,
      color: 'bg-indigo-500 hover:bg-indigo-600',
      onClick: () => console.log('Investimento')
    },
    {
      name: 'Cartão',
      description: 'Transação cartão',
      icon: CreditCard,
      color: 'bg-gray-500 hover:bg-gray-600',
      onClick: () => console.log('Cartão')
    },
  ]

  return (
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
  )
}

export default QuickActions