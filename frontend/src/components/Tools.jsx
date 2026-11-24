import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { post, uploadFile } from '../api.js'

const card = 'rounded-3xl border border-slate-100 bg-white p-8 shadow-sm'
const btn =
  'rounded-xl bg-linear-to-r from-indigo-600 to-fuchsia-500 px-6 py-3 font-bold text-white shadow-md shadow-indigo-200 transition hover:-translate-y-0.5 disabled:opacity-60'
const errBox = 'mt-4 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700'
const md =
  'space-y-2 leading-relaxed text-slate-700 [&_h3]:mt-4 [&_h3]:text-lg [&_h3]:font-bold [&_li]:ml-5 [&_li]:list-disc [&_strong]:font-bold'

function Title({ title, text }) {
  return (
    <div className="mb-6">
      <h2 className="text-2xl font-black tracking-tight">{title}</h2>
      <p className="mt-1 text-slate-600">{text}</p>
    </div>
  )
}

export function UploadPanel({ onUploaded }) {
  const [file, setFile] = useState(null)
  const [inputKey, setInputKey] = useState(0)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  async function handleUpload() {
    if (!file) return
    setBusy(true)
    setError('')
    setMessage('')
    try {
      const data = await uploadFile(file)
      setMessage(`${data.file} uploaded: ${data.pages} pages, ${data.chunks} chunks saved.`)
      setFile(null)
      setInputKey((k) => k + 1)
      onUploaded()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className={card}>
      <Title title="Upload notes" text="Upload your PDF notes. You can add as many files as you need." />
      <input
        key={inputKey}
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0] || null)}
        className="block w-full rounded-2xl border-2 border-dashed border-slate-200 p-6 text-sm text-slate-600 file:mr-4 file:rounded-xl file:border-0 file:bg-indigo-50 file:px-4 file:py-2 file:font-semibold file:text-indigo-700"
      />
      <button onClick={handleUpload} disabled={!file || busy} className={`${btn} mt-6 w-full`}>
        {busy ? 'Uploading and indexing...' : 'Upload PDF'}
      </button>
      {message && (
        <div className="mt-4 rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
          {message}
        </div>
      )}
      {error && <div className={errBox}>{error}</div>}
    </div>
  )
}

export function AskPanel({ source }) {
  const [question, setQuestion] = useState('')
  const [followUp, setFollowUp] = useState(false)
  const [history, setHistory] = useState([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function handleAsk(e) {
    e.preventDefault()
    if (!question.trim()) return
    const last = history[0]?.question
    setBusy(true)
    setError('')
    try {
      const data = await post('/api/ask', {
        source,
        question,
        previous: followUp && last ? last : null,
      })
      setHistory((h) => [{ question, answer: data.answer, pages: data.pages }, ...h])
      setQuestion('')
      setFollowUp(false)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <form onSubmit={handleAsk} className={card}>
        <Title title="Ask from your notes" text={`Source: ${source || 'All files'}`} />
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What is Newton's second law?"
          className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
        />
        <label className="mt-4 flex items-center gap-2 text-sm text-slate-600">
          <input type="checkbox" checked={followUp} onChange={(e) => setFollowUp(e.target.checked)} />
          This is a follow-up to my last question
        </label>
        <button type="submit" disabled={busy || !question.trim()} className={`${btn} mt-6 w-full`}>
          {busy ? 'Searching your notes...' : 'Ask'}
        </button>
        {error && <div className={errBox}>{error}</div>}
      </form>

      <div className="mt-6 space-y-5">
        {history.map((item, i) => (
          <div key={i} className={card}>
            <p className="font-bold">❓ {item.question}</p>
            <div className={`${md} mt-4 border-l-4 border-fuchsia-400 pl-4`}>
              <ReactMarkdown>{item.answer}</ReactMarkdown>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {item.pages.map((p) => (
                <span key={p} className="rounded-lg bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
                  Page {p}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export function SummaryPanel({ source }) {
  const [parts, setParts] = useState([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function handleGenerate() {
    setBusy(true)
    setError('')
    try {
      const data = await post('/api/summary', { source })
      setParts(data.parts)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <div className={card}>
        <Title title="Revision notes" text={`Source: ${source || 'All files'}`} />
        <button onClick={handleGenerate} disabled={busy} className={`${btn} w-full`}>
          {busy ? 'Creating summary...' : 'Generate summary'}
        </button>
        {error && <div className={errBox}>{error}</div>}
      </div>

      <div className="mt-6 space-y-5">
        {parts.map((p, i) => (
          <div key={i} className={card}>
            <h3 className="font-bold text-indigo-700">
              Pages {p.pages[0]} to {p.pages[p.pages.length - 1]}
            </h3>
            <div className={`${md} mt-4`}>
              <ReactMarkdown>{p.summary}</ReactMarkdown>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export function QuizPanel({ source }) {
  const [n, setN] = useState(5)
  const [difficulty, setDifficulty] = useState('medium')
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function handleGenerate() {
    setBusy(true)
    setError('')
    setSubmitted(false)
    setAnswers({})
    try {
      const data = await post('/api/quiz', { source, n, difficulty })
      setQuestions(data.questions)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  const score = questions.reduce((sum, q, i) => sum + (answers[i] === q.answer ? 1 : 0), 0)
  const allAnswered = questions.length > 0 && Object.keys(answers).length === questions.length

  return (
    <div>
      <div className={card}>
        <Title title="Practice quiz" text={`Source: ${source || 'All files'}`} />
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="text-sm font-semibold text-slate-700">
            Number of questions
            <select
              value={n}
              onChange={(e) => setN(Number(e.target.value))}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5"
            >
              {Array.from({ length: 10 }, (_, i) => i + 1).map((v) => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </label>
          <label className="text-sm font-semibold text-slate-700">
            Difficulty
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5"
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </label>
        </div>
        <button onClick={handleGenerate} disabled={busy} className={`${btn} mt-6 w-full`}>
          {busy ? 'Generating questions...' : 'Generate quiz'}
        </button>
        {error && <div className={errBox}>{error}</div>}
      </div>

      <div className="mt-6 space-y-5">
        {questions.map((q, i) => (
          <div key={i} className={card}>
            <p className="font-bold">{i + 1}. {q.question}</p>
            <div className="mt-4 space-y-2">
              {q.options.map((opt, j) => {
                const picked = answers[i] === j
                const isCorrect = submitted && j === q.answer
                const isWrong = submitted && picked && j !== q.answer
                let style = 'border-slate-200 hover:bg-slate-50'
                if (isCorrect) style = 'border-emerald-400 bg-emerald-50'
                else if (isWrong) style = 'border-red-300 bg-red-50'
                else if (picked) style = 'border-indigo-400 bg-indigo-50'
                return (
                  <button
                    key={j}
                    disabled={submitted}
                    onClick={() => setAnswers((a) => ({ ...a, [i]: j }))}
                    className={`block w-full rounded-xl border px-4 py-2.5 text-left text-sm transition ${style}`}
                  >
                    {opt}
                  </button>
                )
              })}
            </div>
            {submitted && <p className="mt-3 text-xs text-slate-500">Source page: {q.page}</p>}
          </div>
        ))}
      </div>

      {questions.length > 0 && !submitted && (
        <button onClick={() => setSubmitted(true)} disabled={!allAnswered} className={`${btn} mt-6 w-full`}>
          Check answers
        </button>
      )}
      {submitted && (
        <div className="mt-6 rounded-2xl bg-indigo-50 p-6 text-lg font-bold text-indigo-700">
          🎉 Score: {score} / {questions.length}
        </div>
      )}
    </div>
  )
}