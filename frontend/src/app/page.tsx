import Link from 'next/link'

const features = [
  {
    title: 'Job Scraping',
    description:
      'Automatically discover and aggregate job listings from multiple platforms.',
    icon: '🔍',
  },
  {
    title: 'Auto-Apply',
    description:
      'Submit applications automatically with AI-optimized cover letters.',
    icon: '🚀',
  },
  {
    title: 'Resume Tailoring',
    description:
      'AI-powered resume customization matched to each job description.',
    icon: '📝',
  },
  {
    title: 'Application Tracking',
    description:
      'Monitor every application status in a centralized dashboard.',
    icon: '📊',
  },
]

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-emerald-400">
            JobAccelerator AI
          </h1>
          <div className="flex items-center space-x-4">
            <Link
              href="/login"
              className="text-gray-300 hover:text-white px-4 py-2 text-sm font-medium transition-colors"
            >
              Login
            </Link>
            <Link
              href="/signup"
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 text-center">
          <h2 className="text-5xl sm:text-6xl font-extrabold tracking-tight">
            <span className="text-emerald-400">JobAccelerator</span> AI
          </h2>
          <p className="mt-6 text-xl sm:text-2xl text-gray-400 max-w-3xl mx-auto">
            AI-Powered Job Application Pipeline
          </p>
          <p className="mt-4 text-lg text-gray-500 max-w-2xl mx-auto">
            Supercharge your job search with intelligent automation. From
            discovery to application, let AI handle the heavy lifting while you
            focus on what matters.
          </p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <Link
              href="/signup"
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors shadow-lg shadow-emerald-600/20"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="border border-gray-700 hover:border-gray-500 text-gray-300 hover:text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
            >
              Login
            </Link>
          </div>
        </section>

        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <h3 className="text-3xl font-bold text-center mb-16">
            Everything you need to land your next role
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature) => (
              <div
                key={feature.title}
                className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-emerald-500/50 transition-colors"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h4 className="text-lg font-semibold mb-2">{feature.title}</h4>
                <p className="text-gray-400 text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="border-t border-gray-800 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
            <h3 className="text-2xl font-bold mb-4">
              Ready to accelerate your job search?
            </h3>
            <p className="text-gray-400 mb-8">
              Join thousands of professionals who automated their path to career
              success.
            </p>
            <Link
              href="/signup"
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors shadow-lg shadow-emerald-600/20"
            >
              Start Free Trial
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
          &copy; {new Date().getFullYear()} JobAccelerator AI. All rights
          reserved.
        </div>
      </footer>
    </div>
  )
}
