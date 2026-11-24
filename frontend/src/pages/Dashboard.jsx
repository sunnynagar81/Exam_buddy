import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { get, getToken, logout } from '../api.js'
import { UploadPanel, AskPanel, SummaryPanel, QuizPanel } from '../components/Tools.jsx'
import StudyPlanPanel from '../components/StudyPlan.jsx'

const TABS = [
  { id: 'overview', label: '🏠 Overview' },
  { id: 'upload', label: '📤 Upload' },
  { id: 'ask', label: '💬 Ask' },
  { id: 'summary', label: '📝 Summary' },
  { id: 'quiz', label: '🧠 Quiz' },
  { id: 'plan', label: '🎯 Study Plan' },
]

const ACTIONS = [
  { id: 'upload', icon: '📤', title: 'Upload notes', text: 'Add PDF files to your library.' },
  { id: 'ask', icon: '💬', title: 'Ask a question', text: 'Get answers with page references.' },
  { id: 'summary', icon: '📝', title: 'Make a summary', text: 'Short revision notes in seconds.' },
  { id: 'quiz', icon: '🧠', title: 'Take a quiz', text: 'Test yourself on your notes.' },
  { id: 'plan', icon: '🎯', title: 'Study plan', text: 'An AI plan for your exam date.' },
]

function Overview({ username, files, onNavigate }) {
  return (
    <div className="space-y-8">
      <div className="rounded-3xl bg-linear-to-r from-indigo-600 via-violet-600 to-fuchsia-500 p-8 text-white shadow-xl shadow-indigo-200">
        <p className="text-sm font-semibold text-indigo-100">Welcome back</p>
        <h1 className="mt-1 text-4xl font-black tracking-tight">{username || '...'} 👋</h1>
        <p className="mt-3 max-w-xl text-indigo-100">
          Keep your revision on track. Upload notes, practice, and plan your exam prep.
        </p>
      </div>

      <div className="grid gap-5 sm:grid-cols-3">
        <div className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Uploaded files</p>
          <p className="mt-2 text-4xl font-black">{files.length}</p>
        </div>
        <div className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-slate-500">AI tools</p>
          <p className="mt-2 text-4xl font-black">5</p>
        </div>
        <div className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-slate-500">Status</p>
          <p className="mt-2 text-4xl font-black text-emerald-600">Ready</p>
        </div>
      </div>

      <div>
        <h2 className="text-xl font-bold">Quick actions</h2>
        <div className="mt-4 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {ACTIONS.map((a) => (
            <button
              key={a.id}
              onClick={() => onNavigate(a.id)}
              className="rounded-3xl border border-slate-100 bg-white p-6 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
            >
              <div className="text-3xl">{a.icon}</div>
              <h3 className="mt-4 font-bold">{a.title}</h3>
              <p className="mt-1 text-sm text-slate-600">{a.text}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [tab, setTab] = useState('overview')
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
      <aside className="sticky top-0 flex h-screen w-64 flex-col border-r border-slate-100 bg-white p-6">
        <Link to="/" className="text-xl font-extrabold">
          📚 Exam <span className="bg-linear-to-r from-indigo-600 to-fuchsia-500 bg-clip-text text-transparent">Buddy</span>
        </Link>

        <nav className="mt-8 space-y-1.5">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`w-full rounded-xl px-4 py-3 text-left font-semibold transition ${
                tab === t.id
                  ? 'bg-linear-to-r from-indigo-50 to-fuchsia-50 text-indigo-700 shadow-sm'
                  : 'text-slate-600 hover:bg-slate-50'
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
        <div className="mx-auto max-w-4xl">
          {tab === 'overview' && <Overview username={username} files={files} onNavigate={setTab} />}
          {tab === 'upload' && <UploadPanel onUploaded={() => setRefreshKey((k) => k + 1)} />}
          {tab === 'ask' && <AskPanel source={source} />}
          {tab === 'summary' && <SummaryPanel source={source} />}
          {tab === 'quiz' && <QuizPanel source={source} />}
          {tab === 'plan' && <StudyPlanPanel />}
        </div>
      </main>
    </div>
  )
}