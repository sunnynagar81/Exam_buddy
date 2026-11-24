import { Link } from 'react-router-dom'

const features = [
  { icon: '📤', title: 'Upload notes', text: 'Save PDF notes by subject. Each subject stays separate.' },
  { icon: '💬', title: 'Ask questions', text: 'Get clear answers with the exact source page for every reply.' },
  { icon: '📝', title: 'Smart summaries', text: 'Short revision notes and key points, section by section.' },
  { icon: '🧠', title: 'Practice quizzes', text: 'Choose the number of questions and difficulty, then check your score.' },
]

const steps = [
  { title: 'Create an account', text: 'Sign up in seconds with a username and password.' },
  { title: 'Upload your notes', text: 'Add your PDF files under a subject name.' },
  { title: 'Study smarter', text: 'Ask, summarize, and quiz yourself from your own material.' },
]

const stats = [
  { value: '4', label: 'Study tools in one place' },
  { value: 'Notes only', label: 'Answers grounded in your files' },
  { value: 'Page-wise', label: 'Source references' },
]

export default function Landing() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      {/* Navbar */}
      <header className="sticky top-0 z-20 border-b border-slate-100 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="text-xl font-extrabold">
            📚 Exam{' '}
            <span className="bg-linear-to-r from-indigo-600 to-fuchsia-500 bg-clip-text text-transparent">Buddy</span>
          </div>
          <nav className="hidden gap-8 text-sm font-semibold text-slate-600 md:flex">
            <a href="#features" className="hover:text-slate-900">Features</a>
            <a href="#how" className="hover:text-slate-900">How it works</a>
          </nav>
          <div className="flex items-center gap-3">
            <Link to="/login" className="rounded-xl px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100">
              Login
            </Link>
            <Link to="/signup" className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700">
              Sign up
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="pointer-events-none absolute -top-40 left-1/2 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-indigo-100 opacity-60 blur-3xl" />
        <div className="relative mx-auto max-w-4xl px-6 pb-20 pt-24 text-center">
          <span className="inline-block rounded-full border border-indigo-100 bg-indigo-50 px-4 py-1.5 text-xs font-semibold text-indigo-700">
            ✨ AI-powered study assistant
          </span>
          <h1 className="mt-6 text-5xl font-black leading-tight tracking-tight md:text-6xl">
            Prepare smarter with{' '}
            <span className="bg-linear-to-r from-indigo-600 via-violet-500 to-fuchsia-500 bg-clip-text text-transparent">
              your own notes
            </span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-slate-600">
            Upload your PDF notes, ask questions, get summaries, and practice quizzes. Every answer comes from your
            material, with page numbers shown.
          </p>
          <div className="mt-10 flex flex-col justify-center gap-4 sm:flex-row">
            <Link
              to="/signup"
              className="rounded-2xl bg-linear-to-r from-indigo-600 to-fuchsia-500 px-8 py-4 font-bold text-white shadow-lg shadow-indigo-200 transition hover:-translate-y-0.5"
            >
              Get started free
            </Link>
            <a href="#how" className="rounded-2xl border border-slate-200 px-8 py-4 font-bold text-slate-700 hover:bg-slate-50">
              See how it works
            </a>
          </div>
          <div className="mt-14 grid grid-cols-1 gap-6 border-t border-slate-100 pt-10 sm:grid-cols-3">
            {stats.map((s) => (
              <div key={s.label}>
                <div className="text-2xl font-extrabold text-slate-900">{s.value}</div>
                <div className="mt-1 text-sm text-slate-500">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="bg-slate-50 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center">
            <p className="text-sm font-bold uppercase tracking-widest text-indigo-600">Features</p>
            <h2 className="mt-3 text-4xl font-black tracking-tight">Everything you need to revise</h2>
          </div>
          <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((f) => (
              <div
                key={f.title}
                className="rounded-3xl border border-slate-100 bg-white p-7 shadow-sm transition hover:-translate-y-1 hover:shadow-xl"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-2xl">{f.icon}</div>
                <h3 className="mt-5 text-lg font-bold">{f.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-600">{f.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center">
            <p className="text-sm font-bold uppercase tracking-widest text-indigo-600">How it works</p>
            <h2 className="mt-3 text-4xl font-black tracking-tight">Three simple steps</h2>
          </div>
          <div className="mt-14 grid gap-8 md:grid-cols-3">
            {steps.map((s, i) => (
              <div key={s.title} className="text-center">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-linear-to-r from-indigo-600 to-fuchsia-500 text-xl font-extrabold text-white">
                  {i + 1}
                </div>
                <h3 className="mt-5 text-lg font-bold">{s.title}</h3>
                <p className="mt-2 text-slate-600">{s.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to action */}
      <section className="px-6 pb-24">
        <div className="mx-auto max-w-5xl rounded-3xl bg-linear-to-r from-indigo-600 via-violet-600 to-fuchsia-500 px-8 py-16 text-center text-white shadow-2xl shadow-indigo-200">
          <h2 className="text-3xl font-black md:text-4xl">Start your exam preparation today</h2>
          <p className="mx-auto mt-4 max-w-xl text-indigo-100">
            Create a free account, upload your notes, and start practicing right away.
          </p>
          <Link to="/signup" className="mt-8 inline-block rounded-2xl bg-white px-8 py-4 font-bold text-indigo-700 transition hover:-translate-y-0.5">
            Create free account
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-100 py-8 text-center text-sm text-slate-500">
        © 2026 Exam Buddy · Built with Python, React and Gemini
      </footer>
    </div>
  )
}