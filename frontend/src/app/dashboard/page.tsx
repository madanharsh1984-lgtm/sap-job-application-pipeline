'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { getToken, apiGet } from '@/lib/api'

interface User {
  id: number
  email: string
  full_name: string
  role: string
}

interface Stats {
  jobs: number
  applications: number
  resumes: number
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [stats, setStats] = useState<Stats>({ jobs: 0, applications: 0, resumes: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    if (!token) {
      router.push('/login')
      return
    }

    const fetchData = async () => {
      try {
        const userRes = await apiGet('/api/auth/me')
        if (!userRes.ok) {
          router.push('/login')
          return
        }
        const userData = await userRes.json()
        setUser(userData)

        const [jobsRes, appsRes, resumesRes] = await Promise.allSettled([
          apiGet('/api/jobs'),
          apiGet('/api/applications'),
          apiGet('/api/resumes'),
        ])

        const getCount = async (result: PromiseSettledResult<Response>) => {
          if (result.status === 'fulfilled' && result.value.ok) {
            const data = await result.value.json()
            return Array.isArray(data) ? data.length : 0
          }
          return 0
        }

        setStats({
          jobs: await getCount(jobsRes),
          applications: await getCount(appsRes),
          resumes: await getCount(resumesRes),
        })
      } catch {
        router.push('/login')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [router])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400 text-lg">Loading...</div>
      </div>
    )
  }

  const statCards = [
    {
      label: 'Total Jobs',
      value: stats.jobs,
      color: 'text-blue-400',
      bg: 'bg-blue-500/10',
      border: 'border-blue-500/20',
    },
    {
      label: 'Applications',
      value: stats.applications,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10',
      border: 'border-emerald-500/20',
    },
    {
      label: 'Resumes',
      value: stats.resumes,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10',
      border: 'border-purple-500/20',
    },
  ]

  const quickActions = [
    { label: 'Add Job', href: '/dashboard/jobs', icon: '➕' },
    { label: 'Upload Resume', href: '/dashboard/resumes', icon: '📄' },
    { label: 'View Applications', href: '/dashboard/applications', icon: '📋' },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">
          Welcome back, {user?.full_name || 'User'}
        </h1>
        <p className="mt-1 text-gray-400">
          Here&apos;s an overview of your job search pipeline.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {statCards.map((card) => (
          <div
            key={card.label}
            className={`${card.bg} border ${card.border} rounded-xl p-6`}
          >
            <p className="text-gray-400 text-sm font-medium">{card.label}</p>
            <p className={`text-4xl font-bold mt-2 ${card.color}`}>
              {card.value}
            </p>
          </div>
        ))}
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {quickActions.map((action) => (
            <Link
              key={action.label}
              href={action.href}
              className="flex items-center gap-3 bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-emerald-500/50 transition-colors group"
            >
              <span className="text-2xl">{action.icon}</span>
              <span className="text-gray-300 group-hover:text-white font-medium">
                {action.label}
              </span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
