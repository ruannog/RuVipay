import { useState, useEffect, useMemo } from 'react'
import { 
  Plus, 
  Search, 
  Filter,
  TrendingUp,
  TrendingDown,
  MoreHorizontal,
  Edit,
  Trash2,
  DollarSign,
  Banknote
} from 'lucide-react'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import InvestmentModal from '../components/InvestmentModal'
import EmptyState from '../components/EmptyState'
import { useInvestments, useDeleteInvestment } from '../hooks/useApi'

interface Investment {
  id: string
  name: string
  type: string
  amount_invested: number
  current_value: number
  purchase_date: string
  description?: string
  user_id?: number
  created_at?: string
  updated_at?: string
  profit_loss?: number
  profit_loss_percentage?: number
}

const Investments = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState<'all' | 'Renda Fixa' | 'Ações' | 'FII' | 'Cripto'>('all')
  const [showFilters, setShowFilters] = useState(false)
  const [investmentModalOpen, setInvestmentModalOpen] = useState(false)
  const [editingInvestment, setEditingInvestment] = useState<Investment | null>(null)

  // Hooks da API com configuração mais agressiva de refetch
  const { data: apiInvestments, isLoading, error, refetch } = useInvestments()
  const deleteInvestmentMutation = useDeleteInvestment()

  // Force refetch when component mounts
  useEffect(() => {
    refetch()
  }, [refetch])

  // Usar apenas os dados da API - sem dados mocados
  const allInvestments = Array.isArray(apiInvestments) ? apiInvestments : []

  // Filtrar investimentos com useMemo para garantir re-renderização
  const investments = useMemo(() => {
    if (!allInvestments || allInvestments.length === 0) return []
    
    return allInvestments.filter(investment => {
      if (!investment) return false
      
      // Filtro por tipo
      const matchesType = filterType === 'all' || investment.type === filterType
      
      // Se não há busca, retornar apenas filtro de tipo
      if (!searchTerm || searchTerm.trim() === '') {
        return matchesType
      }
      
      // Busca simples e segura
      const search = searchTerm.toLowerCase().trim()
      const name = (investment.name || '').toLowerCase()
      const type = (investment.type || '').toLowerCase()
      const description = (investment.description || '').toLowerCase()
      
      const matchesSearch = name.includes(search) || 
                           type.includes(search) || 
                           description.includes(search)
      
      return matchesSearch && matchesType
    })
  }, [allInvestments, searchTerm, filterType])

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
      return format(date, 'dd/MM/yyyy', { locale: ptBR })
    } catch (error) {
      console.error('Erro ao formatar data:', error, dateString)
      return 'Data inválida'
    }
  }

  const handleDeleteInvestment = async (investmentId: string) => {
    if (window.confirm('Tem certeza que deseja excluir este investimento?')) {
      try {
        await deleteInvestmentMutation.mutateAsync(investmentId)
        alert('Investimento excluído com sucesso!')
      } catch (error) {
        console.error('Erro ao excluir investimento:', error)
        alert('Erro ao excluir investimento. Tente novamente.')
      }
    }
  }

  const handleEditInvestment = (investment: Investment) => {
    setEditingInvestment(investment)
    setInvestmentModalOpen(true)
  }

  const handleCloseModal = () => {
    setInvestmentModalOpen(false)
    setEditingInvestment(null)
    // Force refetch after closing modal to get updated data
    setTimeout(() => refetch(), 100)
  }

  const clearSearch = () => {
    setSearchTerm('')
    setFilterType('all')
  }

  // Calcular totais
  const totalInvested = investments.reduce((sum, inv) => sum + inv.amount_invested, 0)
  const totalCurrent = investments.reduce((sum, inv) => sum + inv.current_value, 0)
  const totalProfit = totalCurrent - totalInvested
  const totalProfitPercentage = totalInvested > 0 ? (totalProfit / totalInvested) * 100 : 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Investimentos</h1>
        <div className="flex items-center space-x-3">
          <button 
            onClick={() => setInvestmentModalOpen(true)}
            className="inline-flex items-center rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-500"
          >
            <Plus className="h-4 w-4 mr-1" />
            Novo Investimento
          </button>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-red-700">
                Erro ao carregar investimentos. Usando dados offline.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Summary Cards */}
      {!isLoading && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-4">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <DollarSign className="h-6 w-6 text-blue-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Investido
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {formatCurrency(totalInvested)}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Banknote className="h-6 w-6 text-green-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Valor Atual
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {formatCurrency(totalCurrent)}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  {totalProfit >= 0 ? (
                    <TrendingUp className="h-6 w-6 text-green-400" />
                  ) : (
                    <TrendingDown className="h-6 w-6 text-red-400" />
                  )}
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Lucro/Prejuízo
                    </dt>
                    <dd className={`text-lg font-medium ${totalProfit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {formatCurrency(totalProfit)}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`h-6 w-6 rounded-full ${totalProfitPercentage >= 0 ? 'bg-green-400' : 'bg-red-400'}`} />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Rentabilidade
                    </dt>
                    <dd className={`text-lg font-medium ${totalProfitPercentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {totalProfitPercentage.toFixed(2)}%
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Buscar por nome, tipo, descrição ou data..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-green-500 focus:border-green-500"
                />
                {searchTerm && (
                  <button
                    onClick={clearSearch}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value as any)}
                className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
              >
                <option value="all">Todos os tipos</option>
                <option value="Renda Fixa">Renda Fixa</option>
                <option value="Ações">Ações</option>
                <option value="FII">Fundos Imobiliários</option>
                <option value="Cripto">Criptomoedas</option>
              </select>
              
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="inline-flex items-center rounded-md border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <Filter className="h-4 w-4 mr-1" />
                Filtros
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Investments Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Investimento
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tipo
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Data Compra
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Valor Inicial
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Valor Atual
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rentabilidade
              </th>
              <th className="relative px-6 py-3">
                <span className="sr-only">Ações</span>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {investments.map((investment) => {
              const profitLoss = (investment.profit_loss ?? (investment.current_value - investment.amount_invested))
              const profitPercentage = investment.profit_loss_percentage ?? ((profitLoss / investment.amount_invested) * 100)
              
              return (
                <tr key={investment.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className={`p-2 rounded-full mr-3 ${
                        profitLoss >= 0 ? 'bg-green-100' : 'bg-red-100'
                      }`}>
                        {profitLoss >= 0 ? (
                          <TrendingUp className="h-4 w-4 text-green-600" />
                        ) : (
                          <TrendingDown className="h-4 w-4 text-red-600" />
                        )}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {investment.name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {investment.description || 'Sem descrição'}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      {investment.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(investment.purchase_date)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatCurrency(investment.initial_amount)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {formatCurrency(investment.current_amount)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex flex-col">
                      <span className={profitLoss >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {profitLoss >= 0 ? '+' : ''}{formatCurrency(profitLoss)}
                      </span>
                      <span className={`text-xs ${profitLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {profitPercentage >= 0 ? '+' : ''}{profitPercentage.toFixed(2)}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center space-x-2">
                      <button 
                        onClick={() => handleEditInvestment(investment)}
                        className="text-blue-600 hover:text-blue-900"
                        title="Editar investimento"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button 
                        onClick={() => handleDeleteInvestment(investment.id)}
                        className="text-red-600 hover:text-red-900"
                        title="Excluir investimento"
                        disabled={deleteInvestmentMutation.isPending}
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                      <button className="text-gray-400 hover:text-gray-600">
                        <MoreHorizontal className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>

        {investments.length === 0 && !isLoading && (
          <>
            {searchTerm || filterType !== 'all' ? (
              <EmptyState
                title="Nenhum investimento encontrado"
                description={`Não encontramos investimentos que correspondam aos critérios: "${searchTerm}" ${filterType !== 'all' ? `| Tipo: ${filterType}` : ''}`}
                actionText="Limpar filtros"
                onAction={clearSearch}
                icon={Search}
              />
            ) : (
              <EmptyState
                title="Nenhum investimento cadastrado"
                description="Comece adicionando seu primeiro investimento para acompanhar sua rentabilidade."
                actionText="Adicionar primeiro investimento"
                onAction={() => setInvestmentModalOpen(true)}
                icon={TrendingUp}
              />
            )}
          </>
        )}
      </div>

      {/* Investment Modal */}
      <InvestmentModal 
        isOpen={investmentModalOpen} 
        onClose={handleCloseModal}
        investment={editingInvestment}
      />
    </div>
  )
}

export default Investments