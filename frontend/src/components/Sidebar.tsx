import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  CreditCard, 
  Tags, 
  PieChart,
  TrendingUp,
  Wallet
} from 'lucide-react'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Transações', href: '/transactions', icon: CreditCard },
  { name: 'Categorias', href: '/categories', icon: Tags },
  { name: 'Relatórios', href: '/reports', icon: PieChart },
  { name: 'Metas', href: '/goals', icon: TrendingUp },
]

const Sidebar = () => {
  const location = useLocation()

  return (
    <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-64 lg:flex-col">
      <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-blue-600 px-6 pb-4">
        <div className="flex h-16 shrink-0 items-center">
          <Wallet className="h-8 w-8 text-white" />
          <span className="ml-2 text-xl font-bold text-white">RuViPay</span>
        </div>
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href
                  return (
                    <li key={item.name}>
                      <Link
                        to={item.href}
                        className={clsx(
                          isActive
                            ? 'bg-blue-700 text-white'
                            : 'text-blue-200 hover:text-white hover:bg-blue-700',
                          'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold'
                        )}
                      >
                        <item.icon
                          className={clsx(
                            isActive ? 'text-white' : 'text-blue-200 group-hover:text-white',
                            'h-6 w-6 shrink-0'
                          )}
                          aria-hidden="true"
                        />
                        {item.name}
                      </Link>
                    </li>
                  )
                })}
              </ul>
            </li>
            <li className="mt-auto">
              <div className="bg-blue-700 rounded-lg p-4">
                <h3 className="text-sm font-medium text-white mb-2">
                  Saldo Total
                </h3>
                <p className="text-2xl font-bold text-white">
                  R$ 2.450,00
                </p>
                <p className="text-xs text-blue-200">
                  +R$ 120,00 este mês
                </p>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  )
}

export default Sidebar