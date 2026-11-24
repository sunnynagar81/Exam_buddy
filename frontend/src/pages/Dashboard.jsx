import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { get, getToken, logout } from '../api.js'
import { UploadPanel, AskPanel, SummaryPanel, QuizPanel } from '../components/Tools.jsx'

const TABS = [
  { id: 'upload', label: '📤 Upload' },
  { id: 'ask', label: '💬 Ask' },
  { id: 'summary', label: '📝 Summary' },
  { id: 'quiz', label: '🧠 Quiz' },
]

export default function Dashboard() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [tab, setTab] = useState('upload')
  const [file, setFile] = useState('')
  const [files, setFiles] = useState([])
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    if (!getToken()) {
      navigate('/login')
      return
    }
    get('/api/me')
      .then((d) => setUsername(d.username))
      .catch(() => {
        logout()
        navigate('/login')
      })
  }, [navigate])

  useEffect(() => {
    get('/api/files')
      .then((d) => setFiles(d.files))
      .catch(() => setFiles([]))
  }, [refreshKey])

  function handleLogout() {
    logout()
    navigate('/')
  }

  const source = file || null

  return (
    <div className="flex min-h-screen bg-slate-50">
      <aside className="flex w-64 flex-col border-r border-slate-100 bg-white p-6">
        <Link to="/" className="text-xl font-extrabold">
          📚 Exam <span className="bg-linear-to-r from-indigo-600 to-fuchsia-500 bg-clip-text text-transparent">Buddy</span>
        </Link>

        <nav className="mt-8 space-y-2">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`w-full rounded-xl px-4 py-3 text-left font-semibold transition ${
                tab === t.id ? 'bg-indigo-50 text-indigo-700' : 'text-slate-600 hover:bg-slate-50'
              }`}
            >
              {t.label}
            </button>
          ))}
        </nav>

        <div className="mt-8 border-t border-slate-100 pt-6">
          <label className="block text-sm font-semibold text-slate-700">
            Choose file
            <select
              value={file}
              onChange={(e) => setFile(e.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 outline-none focus:border-indigo-500"
            >
              <option value="">All files</option>
              {files.map((f) => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </label>
          <p className="mt-2 text-xs text-slate-500">{files.length} file(s) uploaded</p>
        </div>

        <button
          onClick={handleLogout}
          className="mt-auto rounded-xl px-4 py-3 text-left font-semibold text-slate-600 hover:bg-slate-50"
        >
          🚪 Logout
        </button>
      </aside>

      <main className="flex-1 p-10">
        <h1 className="text-3xl font-black tracking-tight">Welcome, {username || '...'} 👋</h1>
        <p className="mt-2 text-slate-600">Upload your notes, then ask questions, get summaries, and practice quizzes.</p>

        <div className="mt-8 max-w-3xl">
          {tab === 'upload' && <UploadPanel onUploaded={() => setRefreshKey((k) => k + 1)} />}
          {tab === 'ask' && <AskPanel source={source} />}
          {tab === 'summary' && <SummaryPanel source={source} />}
          {tab === 'quiz' && <QuizPanel source={source} />}
        </div>
      </main>
    </div>
  )
}