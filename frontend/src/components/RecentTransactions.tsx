import { ArrowUpIcon, ArrowDownIcon, MoreHorizontal } from 'lucide-react'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'

interface Transaction {
  id: string
  description: string
  amount: number
  type: 'income' | 'expense'
  category: string
  date: string
}

interface RecentTransactionsProps {
  transactions?: Transaction[]
}

const RecentTransactions = ({ transactions: propTransactions }: RecentTransactionsProps) => {
  // Usar dados da API se disponíveis, senão usar mock data
  const transactions: Transaction[] = propTransactions || [
    {
      id: '1',
      description: 'Salário',
      amount: 3500.00,
      type: 'income',
      category: 'Salário',
      date: '2024-01-15'
    },
    {
      id: '2',
      description: 'Supermercado',
      amount: 280.50,
      type: 'expense',
      category: 'Alimentação',
      date: '2024-01-14'
    },
    {
      id: '3',
      description: 'Freelance',
      amount: 1200.00,
      type: 'income',
      category: 'Trabalho',
      date: '2024-01-13'
    },
    {
      id: '4',
      description: 'Combustível',
      amount: 120.00,
      type: 'expense',
      category: 'Transporte',
      date: '2024-01-12'
    },
    {
      id: '5',
      description: 'Academia',
      amount: 89.90,
      type: 'expense',
      category: 'Saúde',
      date: '2024-01-11'
    }
  ]

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return format(new Date(dateString), 'dd/MM', { locale: ptBR })
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">
          Transações Recentes
        </h3>
        <button className="text-sm text-blue-600 hover:text-blue-500">
          Ver todas
        </button>
      </div>

      <div className="space-y-3">
        {transactions.map((transaction) => (
          <div
            key={transaction.id}
            className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0"
          >
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-full ${
                transaction.type === 'income' 
                  ? 'bg-green-100' 
                  : 'bg-red-100'
              }`}>
                {transaction.type === 'income' ? (
                  <ArrowUpIcon className="h-4 w-4 text-green-600" />
                ) : (
                  <ArrowDownIcon className="h-4 w-4 text-red-600" />
                )}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {transaction.description}
                </p>
                <p className="text-xs text-gray-500">
                  {transaction.category} • {formatDate(transaction.date)}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className={`text-sm font-semibold ${
                transaction.type === 'income' 
                  ? 'text-green-600' 
                  : 'text-red-600'
              }`}>
                {transaction.type === 'income' ? '+' : '-'}
                {formatCurrency(transaction.amount)}
              </span>
              <button className="p-1 hover:bg-gray-100 rounded">
                <MoreHorizontal className="h-4 w-4 text-gray-400" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {transactions.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500 text-sm">
            Nenhuma transação encontrada
          </p>
        </div>
      )}
    </div>
  )
}

export default RecentTransactions