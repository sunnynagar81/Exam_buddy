import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { post } from '../api.js'

const card = 'rounded-3xl border border-slate-100 bg-white p-8 shadow-sm'
const btn =
  'rounded-xl bg-linear-to-r from-indigo-600 to-fuchsia-500 px-6 py-3 font-bold text-white shadow-md shadow-indigo-200 transition hover:-translate-y-0.5 disabled:opacity-60'
const input =
  'mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none transition focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100'
const md =
  'space-y-2 leading-relaxed text-slate-700 [&_h3]:mt-6 [&_h3]:text-xl [&_h3]:font-black [&_h4]:mt-5 [&_h4]:text-lg [&_h4]:font-bold [&_h4]:text-indigo-700 [&_li]:ml-5 [&_li]:list-disc [&_li]:py-0.5 [&_strong]:font-bold'

const today = new Date().toLocaleDateString('en-CA')

export default function StudyPlanPanel() {
  const [exam, setExam] = useState('')
  const [examDate, setExamDate] = useState('')
  const [hours, setHours] = useState(2)
  const [request, setRequest] = useState('')
  const [plan, setPlan] = useState('')
  const [daysLeft, setDaysLeft] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function handleCreate(e) {
    e.preventDefault()
    setBusy(true)
    setError('')
    setPlan('')
    try {
      const data = await post('/api/study-plan', {
        exam,
        exam_date: examDate,
        hours: Number(hours),
        request,
      })
      setPlan(data.plan)
      setDaysLeft(data.days_left)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleCreate} className={card}>
        <h2 className="text-2xl font-black tracking-tight">Build my study plan</h2>
        <p className="mt-1 text-slate-600">
          Tell us about your exam. The AI plans your days using your uploaded notes.
        </p>

        <div className="mt-6 grid gap-5 sm:grid-cols-2">
          <label className="text-sm font-semibold text-slate-700">
            Exam name
            <input
              className={input}
              value={exam}
              onChange={(e) => setExam(e.target.value)}
              placeholder="e.g. End-sem Physics"
              required
            />
          </label>
          <label className="text-sm font-semibold text-slate-700">
            Exam date
            <input
              type="date"
              className={input}
              value={examDate}
              min={today}
              onChange={(e) => setExamDate(e.target.value)}
              required
            />
          </label>
          <label className="text-sm font-semibold text-slate-700">
            Study hours per day
            <input
              type="number"
              min="1"
              max="12"
              className={input}
              value={hours}
              onChange={(e) => setHours(e.target.value)}
            />
          </label>
        </div>

        <label className="mt-5 block text-sm font-semibold text-slate-700">
          Anything else? <span className="font-normal text-slate-500">(optional)</span>
          <textarea
            rows={3}
            className={input}
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            placeholder="e.g. I am weak in numericals. Keep Sundays light."
          />
        </label>

        <button type="submit" disabled={busy || !exam || !examDate} className={`${btn} mt-6 w-full`}>
          {busy ? 'Creating your plan...' : 'Create study plan'}
        </button>
        {error && (
          <div className="mt-4 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
        )}
      </form>

      {plan && (
        <div className={card}>
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-xl font-black">Your plan for {exam}</h3>
            <span className="rounded-full bg-indigo-50 px-4 py-1.5 text-sm font-semibold text-indigo-700">
              {daysLeft} days left
            </span>
          </div>
          <div className={`${md} mt-4`}>
            <ReactMarkdown>{plan}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  )
}