import { ArrowUpIcon, ArrowDownIcon, MoreHorizontal, TrendingUp } from 'lucide-react'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import type { Transaction } from '../services/api'
import EmptyState from './EmptyState'

interface RecentTransactionsProps {
  transactions?: Transaction[]
}

const RecentTransactions = ({ transactions: propTransactions }: RecentTransactionsProps) => {
  // Usar dados da API se disponíveis, senão usar array vazio
  const transactions: Transaction[] = propTransactions || []

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return 'Data inválida'
    
    try {
      const date = new Date(dateString)
      if (isNaN(date.getTime())) {
        return 'Data inválida'
      }
      return format(date, 'dd/MM', { locale: ptBR })
    } catch (error) {
      console.error('Erro ao formatar data:', error, dateString)
      return 'Data inválida'
    }
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
                  {transaction.category || 'Sem categoria'} • {formatDate(transaction.date)}
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
        <EmptyState
          title="Nenhuma transação"
          description="Suas transações recentes aparecerão aqui quando você adicionar algumas."
          icon={TrendingUp}
        />
      )}
    </div>
  )
}

export default RecentTransactions