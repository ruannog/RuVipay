import { useState, useEffect } from 'react'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  CreditCard,
  Plus,
  Wifi,
  WifiOff
} from 'lucide-react'
import TransactionChart from '../components/TransactionChart'
import RecentTransactions from '../components/RecentTransactions'
import QuickActions from '../components/QuickActions'
import { useDashboardStats, useChartData, useHealthCheck } from '../hooks/useApi'

const Dashboard = () => {
  const [period, setPeriod] = useState('30d')
  const [isOnline, setIsOnline] = useState(true)

  // Usar hooks personalizados
  const { 
    data: statsData, 
    isLoading: statsLoading, 
    error: statsError 
  } = useDashboardStats()

  const { 
    data: chartData, 
    isLoading: chartLoading 
  } = useChartData(period)

  const { 
    error: healthError
  } = useHealthCheck()

  useEffect(() => {
    setIsOnline(!healthError)
  }, [healthError])

  // Se não conseguir conectar com a API, usar dados mock
  const stats = statsData ? [
    {
      name: 'Receitas',
      value: `R$ ${statsData.totalIncome.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
      change: '+12%',
      changeType: 'positive' as const,
      icon: TrendingUp,
    },
    {
      name: 'Despesas',
      value: `R$ ${statsData.totalExpense.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
      change: '-8%',
      changeType: 'negative' as const,
      icon: TrendingDown,
    },
    {
      name: 'Saldo',
      value: `R$ ${statsData.balance.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`,
      change: '+23%',
      changeType: statsData.balance >= 0 ? 'positive' as const : 'negative' as const,
      icon: DollarSign,
    },
    {
      name: 'Transações',
      value: statsData.transactionCount.toString(),
      change: '+3',
      changeType: 'positive' as const,
      icon: CreditCard,
    },
  ] : [
    {
      name: 'Receitas',
      value: 'R$ 3.240,00',
      change: '+12%',
      changeType: 'positive' as const,
      icon: TrendingUp,
    },
    {
      name: 'Despesas',
      value: 'R$ 1.890,00',
      change: '-8%',
      changeType: 'negative' as const,
      icon: TrendingDown,
    },
    {
      name: 'Saldo',
      value: 'R$ 1.350,00',
      change: '+23%',
      changeType: 'positive' as const,
      icon: DollarSign,
    },
    {
      name: 'Transações',
      value: '47',
      change: '+3',
      changeType: 'positive' as const,
      icon: CreditCard,
    },
  ]

  return (
    <div className="space-y-6">
      {/* Status de Conexão */}
      {!isOnline && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <div className="flex">
            <WifiOff className="h-5 w-5 text-yellow-400" />
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                Sem conexão com o servidor. Exibindo dados offline.
              </p>
            </div>
          </div>
        </div>
      )}

      {isOnline && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <div className="flex">
            <Wifi className="h-5 w-5 text-green-400" />
            <div className="ml-3">
              <p className="text-sm text-green-700">
                ✅ Conectado ao backend RuViPay!
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex items-center space-x-3">
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="7d">Últimos 7 dias</option>
            <option value="30d">Últimos 30 dias</option>
            <option value="90d">Últimos 90 dias</option>
            <option value="1y">Último ano</option>
          </select>
          <button className="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">
            <Plus className="h-4 w-4 mr-1" />
            Nova Transação
          </button>
        </div>
      </div>

      {/* Loading State */}
      {statsLoading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Stats Cards */}
      {!statsLoading && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <div
              key={stat.name}
              className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:px-6 sm:py-6"
            >
              <dt>
                <div className="absolute rounded-md bg-blue-500 p-3">
                  <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <p className="ml-16 truncate text-sm font-medium text-gray-500">
                  {stat.name}
                </p>
              </dt>
              <dd className="ml-16 flex items-baseline">
                <p className="text-2xl font-semibold text-gray-900">
                  {stat.value}
                </p>
                <p
                  className={`ml-2 flex items-baseline text-sm font-semibold ${
                    stat.changeType === 'positive' 
                      ? 'text-green-600' 
                      : 'text-red-600'
                  }`}
                >
                  {stat.change}
                </p>
              </dd>
            </div>
          ))}
        </div>
      )}

      {/* Charts and Recent Transactions */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Resumo Financeiro {chartLoading && <span className="text-sm text-gray-500">(Carregando...)</span>}
          </h3>
          <TransactionChart period={period} chartData={chartData} />
        </div>
        
        <div className="rounded-lg bg-white p-6 shadow">
          <RecentTransactions transactions={statsData?.recentTransactions} />
        </div>
      </div>

      {/* Quick Actions */}
      <QuickActions />
    </div>
  )
}

export default Dashboard