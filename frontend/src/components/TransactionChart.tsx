import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'
import { useState } from 'react'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface TransactionChartProps {
  period: string
  chartData?: {
    labels: string[]
    income: number[]
    expense: number[]
  }
}

const TransactionChart = ({ period, chartData }: TransactionChartProps) => {
  const [chartType, setChartType] = useState<'line' | 'bar'>('line')

  // Usar dados da API se disponíveis, senão usar mock data
  const labels = chartData?.labels || ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
  const incomeData = chartData?.income || [3200, 2800, 3500, 4200, 3800, 3240]
  const expenseData = chartData?.expense || [2100, 1900, 2300, 2800, 2200, 1890]
  
  const data = {
    labels,
    datasets: [
      {
        label: 'Receitas',
        data: incomeData,
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        tension: 0.1,
      },
      {
        label: 'Despesas',
        data: expenseData,
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.2)',
        tension: 0.1,
      },
    ],
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value: any) {
            return 'R$ ' + value.toLocaleString('pt-BR')
          }
        }
      }
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h4 className="text-sm font-medium text-gray-700">
          Período: {period}
        </h4>
        <div className="flex space-x-2">
          <button
            onClick={() => setChartType('line')}
            className={`px-3 py-1 text-xs rounded ${
              chartType === 'line'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            Linha
          </button>
          <button
            onClick={() => setChartType('bar')}
            className={`px-3 py-1 text-xs rounded ${
              chartType === 'bar'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            Barras
          </button>
        </div>
      </div>
      
      <div style={{ height: '300px' }}>
        {chartType === 'line' ? (
          <Line data={data} options={options} />
        ) : (
          <Bar data={data} options={options} />
        )}
      </div>
    </div>
  )
}

export default TransactionChart