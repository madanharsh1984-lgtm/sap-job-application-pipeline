'use client'

import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { getToken, apiGet, apiRequest } from '@/lib/api'

interface Resume {
  id: number
  filename: string
  version: string
  is_tailored: boolean
  created_at: string
}

export default function ResumesPage() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    if (!getToken()) {
      router.push('/login')
      return
    }
    fetchResumes()
  }, [router])

  const fetchResumes = async () => {
    try {
      const res = await apiGet('/api/resumes')
      if (res.ok) {
        const data = await res.json()
        setResumes(Array.isArray(data) ? data : [])
      }
    } catch {
      // silently handle
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const res = await apiRequest('/api/resumes/upload', {
        method: 'POST',
        body: formData,
      })

      if (res.ok) {
        fetchResumes()
      }
    } catch {
      // silently handle
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr).toLocaleDateString()
    } catch {
      return dateStr
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400 text-lg">Loading resumes...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-white">Resumes</h1>
        <div>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleUpload}
            className="hidden"
            id="resume-upload"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-emerald-800 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {uploading ? 'Uploading...' : '📄 Upload Resume'}
          </button>
        </div>
      </div>

      {resumes.length === 0 ? (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
          <p className="text-gray-400 text-lg">No resumes uploaded.</p>
          <p className="text-gray-500 mt-2">
            Upload your resume to get started with AI-powered tailoring.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="text-2xl">📄</div>
                  <div>
                    <p className="text-white font-medium text-sm truncate max-w-[180px]">
                      {resume.filename}
                    </p>
                    <p className="text-gray-500 text-xs mt-0.5">
                      {resume.version && `v${resume.version}`}
                      {resume.version && ' · '}
                      {formatDate(resume.created_at)}
                    </p>
                  </div>
                </div>
                {resume.is_tailored && (
                  <span className="inline-flex px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-400">
                    Tailored
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
