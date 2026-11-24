import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { post, saveToken } from '../api.js'

const inputClass =
  'mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none transition focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100'

export default function Auth({ mode }) {
  const navigate = useNavigate()
  const isLogin = mode === 'login'

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!isLogin && password !== confirm) {
      setError('Passwords do not match.')
      return
    }

    setLoading(true)
    try {
      if (!isLogin) {
        await post('/api/signup', { username, password })
      }
      const data = await post('/api/login', { username, password })
      saveToken(data.token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-6">
      <div className="w-full max-w-md rounded-3xl border border-slate-100 bg-white p-8 shadow-xl shadow-slate-200/60">
        <Link to="/" className="text-xl font-extrabold">
          📚 Exam <span className="bg-linear-to-r from-indigo-600 to-fuchsia-500 bg-clip-text text-transparent">Buddy</span>
        </Link>

        <h1 className="mt-8 text-3xl font-black tracking-tight">
          {isLogin ? 'Welcome back' : 'Create your account'}
        </h1>
        <p className="mt-2 text-slate-600">
          {isLogin ? 'Login to continue your revision.' : 'Sign up free and start studying smarter.'}
        </p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          <div>
            <label className="text-sm font-semibold text-slate-700">Username</label>
            <input
              className={inputClass}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. sunny123"
              required
            />
            {!isLogin && (
              <p className="mt-1 text-xs text-slate-500">Only letters and numbers, 3 to 20 characters.</p>
            )}
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700">Password</label>
            <input
              type="password"
              className={inputClass}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="At least 6 characters"
              required
            />
          </div>

          {!isLogin && (
            <div>
              <label className="text-sm font-semibold text-slate-700">Confirm password</label>
              <input
                type="password"
                className={inputClass}
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                required
              />
            </div>
          )}

          {error && (
            <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-linear-to-r from-indigo-600 to-fuchsia-500 py-3.5 font-bold text-white shadow-lg shadow-indigo-200 transition hover:-translate-y-0.5 disabled:opacity-60"
          >
            {loading ? 'Please wait...' : isLogin ? 'Login' : 'Create account'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-600">
          {isLogin ? (
            <>
              New here?{' '}
              <Link to="/signup" className="font-semibold text-indigo-600 hover:underline">Create an account</Link>
            </>
          ) : (
            <>
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-indigo-600 hover:underline">Login</Link>
            </>
          )}
        </p>
      </div>
    </div>
  )
}