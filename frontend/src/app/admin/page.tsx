'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { getToken, apiGet, apiPut } from '@/lib/api'

interface User {
  id: number
  email: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
}

interface SystemStats {
  total_users: number
  total_jobs: number
  total_applications: number
  total_resumes: number
}

interface LogEntry {
  id: number
  message: string
  level: string
  created_at: string
}

export default function AdminPage() {
  const router = useRouter()
  const [users, setUsers] = useState<User[]>([])
  const [stats, setStats] = useState<SystemStats | null>(null)
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'users' | 'stats' | 'logs'>(
    'users'
  )

  useEffect(() => {
    const token = getToken()
    if (!token) {
      router.push('/login')
      return
    }

    const checkAdmin = async () => {
      try {
        const userRes = await apiGet('/api/auth/me')
        if (!userRes.ok) {
          router.push('/login')
          return
        }
        const userData = await userRes.json()
        if (userData.role !== 'admin') {
          router.push('/dashboard')
          return
        }

        const [usersRes, statsRes, logsRes] = await Promise.allSettled([
          apiGet('/api/admin/users'),
          apiGet('/api/admin/stats'),
          apiGet('/api/admin/logs'),
        ])

        if (usersRes.status === 'fulfilled' && usersRes.value.ok) {
          const data = await usersRes.value.json()
          setUsers(Array.isArray(data) ? data : [])
        }
        if (statsRes.status === 'fulfilled' && statsRes.value.ok) {
          setStats(await statsRes.value.json())
        }
        if (logsRes.status === 'fulfilled' && logsRes.value.ok) {
          const data = await logsRes.value.json()
          setLogs(Array.isArray(data) ? data : [])
        }
      } catch {
        router.push('/dashboard')
      } finally {
        setLoading(false)
      }
    }

    checkAdmin()
  }, [router])

  const handleRoleChange = async (userId: number, newRole: string) => {
    try {
      const res = await apiPut(`/api/admin/users/${userId}/role`, {
        role: newRole,
      })
      if (res.ok) {
        setUsers(
          users.map((u) => (u.id === userId ? { ...u, role: newRole } : u))
        )
      }
    } catch {
      // silently handle
    }
  }

  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr).toLocaleString()
    } catch {
      return dateStr
    }
  }

  const logLevelColors: Record<string, string> = {
    info: 'text-blue-400',
    warning: 'text-yellow-400',
    error: 'text-red-400',
    debug: 'text-gray-400',
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-gray-400 text-lg">Loading admin panel...</div>
      </div>
    )
  }

  const tabs = [
    { id: 'users' as const, label: 'Users' },
    { id: 'stats' as const, label: 'System Stats' },
    { id: 'logs' as const, label: 'Recent Logs' },
  ]

  return (
    <div className="min-h-screen bg-gray-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Admin Panel</h1>
          <p className="mt-1 text-gray-400">
            Manage users, view system stats, and monitor logs.
          </p>
        </div>

        <div className="flex space-x-1 bg-gray-900 rounded-lg p-1 mb-8 w-fit">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === 'users' && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-800">
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Email
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Role
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Joined
                    </th>
                    <th className="text-left px-6 py-3 text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800">
                  {users.map((user) => (
                    <tr
                      key={user.id}
                      className="hover:bg-gray-800/50 transition-colors"
                    >
                      <td className="px-6 py-4 text-sm text-white font-medium">
                        {user.full_name}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-300">
                        {user.email}
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            user.role === 'admin'
                              ? 'bg-yellow-500/20 text-yellow-400'
                              : 'bg-blue-500/20 text-blue-400'
                          }`}
                        >
                          {user.role}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            user.is_active
                              ? 'bg-emerald-500/20 text-emerald-400'
                              : 'bg-red-500/20 text-red-400'
                          }`}
                        >
                          {user.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-400">
                        {formatDate(user.created_at)}
                      </td>
                      <td className="px-6 py-4">
                        <select
                          value={user.role}
                          onChange={(e) =>
                            handleRoleChange(user.id, e.target.value)
                          }
                          className="bg-gray-800 border border-gray-700 rounded-md text-sm text-gray-300 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                          aria-label={`Change role for ${user.full_name}`}
                        >
                          <option value="user">User</option>
                          <option value="admin">Admin</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {users.length === 0 && (
              <div className="p-8 text-center text-gray-400">
                No users found.
              </div>
            )}
          </div>
        )}

        {activeTab === 'stats' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                label: 'Total Users',
                value: stats?.total_users ?? 0,
                color: 'text-blue-400',
                bg: 'bg-blue-500/10',
                border: 'border-blue-500/20',
              },
              {
                label: 'Total Jobs',
                value: stats?.total_jobs ?? 0,
                color: 'text-emerald-400',
                bg: 'bg-emerald-500/10',
                border: 'border-emerald-500/20',
              },
              {
                label: 'Total Applications',
                value: stats?.total_applications ?? 0,
                color: 'text-purple-400',
                bg: 'bg-purple-500/10',
                border: 'border-purple-500/20',
              },
              {
                label: 'Total Resumes',
                value: stats?.total_resumes ?? 0,
                color: 'text-yellow-400',
                bg: 'bg-yellow-500/10',
                border: 'border-yellow-500/20',
              },
            ].map((card) => (
              <div
                key={card.label}
                className={`${card.bg} border ${card.border} rounded-xl p-6`}
              >
                <p className="text-gray-400 text-sm font-medium">
                  {card.label}
                </p>
                <p className={`text-4xl font-bold mt-2 ${card.color}`}>
                  {card.value}
                </p>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'logs' && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
            {logs.length === 0 ? (
              <div className="p-8 text-center text-gray-400">
                No recent logs.
              </div>
            ) : (
              <div className="divide-y divide-gray-800">
                {logs.map((log) => (
                  <div
                    key={log.id}
                    className="px-6 py-3 flex items-start gap-4 hover:bg-gray-800/50"
                  >
                    <span
                      className={`text-xs font-mono uppercase font-medium mt-0.5 min-w-[60px] ${
                        logLevelColors[log.level?.toLowerCase()] ||
                        'text-gray-400'
                      }`}
                    >
                      {log.level}
                    </span>
                    <span className="text-sm text-gray-300 flex-1">
                      {log.message}
                    </span>
                    <span className="text-xs text-gray-500 whitespace-nowrap">
                      {formatDate(log.created_at)}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
