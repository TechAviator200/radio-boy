import Link from "next/link";
import { getAgent } from "@/lib/agents";

export default function Page() {
  const agent = getAgent("radioboy");
  if (!agent) return <main className="p-8">Agent not found</main>;

  const isLive = agent.demoUrl && agent.demoUrl !== "#";

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#1a1f2e]">
      {/* Background doodle pattern */}
      <svg
        className="pointer-events-none absolute inset-0 h-full w-full opacity-[0.12]"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <pattern
            id="radioboy-doodles"
            width="200"
            height="200"
            patternUnits="userSpaceOnUse"
          >
            {/* Music notes */}
            <path
              d="M20 30 Q25 25 25 35 M25 35 L25 20 M25 20 Q30 18 30 22"
              stroke="#3dd9d9"
              strokeWidth="1"
              fill="none"
            />
            <path
              d="M170 50 Q175 45 175 55 M175 55 L175 40 M175 40 Q180 38 180 42"
              stroke="#3dd9d9"
              strokeWidth="1"
              fill="none"
            />
            {/* Headphones */}
            <path d="M60 80 Q60 60 80 60 Q100 60 100 80" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            <ellipse cx="60" cy="85" rx="6" ry="10" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            <ellipse cx="100" cy="85" rx="6" ry="10" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            {/* Sound waves */}
            <path d="M150 100 Q155 95 155 100 Q155 105 150 100" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            <path d="M158 95 Q165 88 165 100 Q165 112 158 105" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            <path d="M168 90 Q178 80 178 100 Q178 120 168 110" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            {/* Vinyl record */}
            <circle cx="40" cy="150" r="20" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            <circle cx="40" cy="150" r="8" stroke="#3dd9d9" strokeWidth="0.5" fill="none" />
            <circle cx="40" cy="150" r="3" fill="#3dd9d9" opacity="0.3" />
            {/* Microphone */}
            <ellipse cx="160" cy="160" rx="8" ry="12" stroke="#3dd9d9" strokeWidth="1" fill="none" />
            <path d="M160 172 L160 185 M152 185 L168 185" stroke="#3dd9d9" strokeWidth="1" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#radioboy-doodles)" />
      </svg>

      {/* Navigation */}
      <nav className="relative z-10 flex items-center justify-between px-8 py-6">
        <Link href="/" className="text-xl font-bold text-white">
          Portfolio
        </Link>
        <div className="flex items-center gap-8">
          <Link href="/" className="text-sm text-zinc-300 transition-colors hover:text-white">
            Home
          </Link>
          <Link href="/projects" className="text-sm text-zinc-300 transition-colors hover:text-white">
            Projects
          </Link>
          <Link href="/projects#contact" className="text-sm text-zinc-300 transition-colors hover:text-white">
            Contact
          </Link>
        </div>
      </nav>

      <main className="relative z-10 mx-auto max-w-6xl px-8 py-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Breadcrumb */}
        <Link
          href="/media-entertainment"
          className="mb-8 inline-flex items-center gap-2 text-sm text-zinc-300 transition-colors hover:text-[#3dd9d9] active:scale-[0.98]"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Media & Entertainment
        </Link>

        <div className="grid gap-12 lg:grid-cols-2">
          {/* Left side - Illustration */}
          <div className="flex items-center justify-center rounded-2xl bg-white p-8">
            <svg viewBox="0 0 300 280" fill="none" className="h-full w-full max-w-md">
              {/* Person with headphones and radio equipment */}
              {/* Background elements */}
              <circle cx="250" cy="50" r="25" fill="#3dd9d9" opacity="0.1" />
              <circle cx="50" cy="230" r="20" fill="#3dd9d9" opacity="0.1" />

              {/* Radio/Audio equipment - Left side */}
              <rect x="20" y="100" width="80" height="60" rx="8" fill="#2a3142" />
              <rect x="28" y="108" width="64" height="35" rx="4" fill="#1a1f2e" />
              {/* Frequency display */}
              <rect x="35" y="115" width="50" height="12" rx="2" fill="#3dd9d9" opacity="0.3" />
              <text x="45" y="124" fill="#3dd9d9" fontSize="8" fontFamily="monospace">98.7 FM</text>
              {/* Buttons */}
              <circle cx="40" cy="135" r="4" fill="#3dd9d9" />
              <circle cx="55" cy="135" r="4" fill="#ff9f43" opacity="0.6" />
              <circle cx="70" cy="135" r="4" fill="#3dd9d9" opacity="0.5" />
              {/* Volume slider */}
              <rect x="28" y="150" width="64" height="4" rx="2" fill="#1a1f2e" />
              <rect x="28" y="150" width="40" height="4" rx="2" fill="#3dd9d9" />

              {/* Person */}
              {/* Head */}
              <ellipse cx="180" cy="100" rx="30" ry="28" fill="#fbd5c8" />
              {/* Hair */}
              <ellipse cx="180" cy="80" rx="35" ry="25" fill="#3dd9d9" />
              <path d="M145 95 Q160 70 180 65 Q200 70 215 95" fill="#3dd9d9" />

              {/* Headphones */}
              <path d="M145 100 Q145 70 180 70 Q215 70 215 100" stroke="#2a3142" strokeWidth="6" fill="none" />
              <ellipse cx="145" cy="105" rx="10" ry="15" fill="#2a3142" />
              <ellipse cx="215" cy="105" rx="10" ry="15" fill="#2a3142" />
              <ellipse cx="145" cy="105" rx="6" ry="10" fill="#3dd9d9" opacity="0.3" />
              <ellipse cx="215" cy="105" rx="6" ry="10" fill="#3dd9d9" opacity="0.3" />

              {/* Body */}
              <path d="M150 130 Q145 170 150 210 L210 210 Q215 170 210 130 Q180 145 150 130" fill="white" />

              {/* Arms */}
              <path d="M150 145 Q120 160 100 160" stroke="#fbd5c8" strokeWidth="14" strokeLinecap="round" />
              <path d="M210 145 Q240 160 260 180" stroke="#fbd5c8" strokeWidth="14" strokeLinecap="round" />

              {/* Microphone on stand */}
              <rect x="240" y="120" width="4" height="80" fill="#2a3142" />
              <ellipse cx="242" cy="110" rx="12" ry="18" fill="#2a3142" />
              <ellipse cx="242" cy="110" rx="8" ry="12" fill="#3dd9d9" opacity="0.2" />
              {/* Mic mesh pattern */}
              <path d="M235 105 L249 105 M235 110 L249 110 M235 115 L249 115" stroke="#3dd9d9" strokeWidth="0.5" opacity="0.5" />

              {/* Sound waves from speaker */}
              <path d="M100 125 Q105 120 105 125 Q105 130 100 125" stroke="#3dd9d9" strokeWidth="1.5" fill="none" />
              <path d="M108 118 Q116 110 116 125 Q116 140 108 132" stroke="#3dd9d9" strokeWidth="1.5" fill="none" />
              <path d="M118 112 Q130 100 130 125 Q130 150 118 138" stroke="#3dd9d9" strokeWidth="1.5" fill="none" />

              {/* Legs */}
              <path d="M160 210 Q150 240 155 270" stroke="#3dd9d9" strokeWidth="18" strokeLinecap="round" />
              <path d="M200 210 Q210 240 205 270" stroke="#3dd9d9" strokeWidth="18" strokeLinecap="round" />

              {/* Shoes */}
              <ellipse cx="155" cy="275" rx="15" ry="6" fill="white" />
              <ellipse cx="205" cy="275" rx="15" ry="6" fill="white" />

              {/* Floating music notes */}
              <path d="M270 60 Q275 55 275 65 M275 65 L275 45 Q282 42 282 48" stroke="#3dd9d9" strokeWidth="2" fill="none" />
              <path d="M30 50 Q35 45 35 55 M35 55 L35 40 Q42 37 42 43" stroke="#3dd9d9" strokeWidth="2" fill="none" />
            </svg>
          </div>

          {/* Right side - Content */}
          <div className="flex flex-col justify-center">
            {/* Tags */}
            <div className="mb-4 flex flex-wrap gap-2">
              {agent.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full border border-zinc-700 bg-zinc-800/50 px-3 py-1 text-xs text-zinc-300"
                >
                  {tag}
                </span>
              ))}
            </div>

            <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
              <span className="text-[#3dd9d9]">{agent.title}</span>
            </h1>
            <p className="mt-4 text-lg text-zinc-300">{agent.description}</p>

            {/* What it does */}
            <div className="mt-8">
              <h2 className="text-xl font-semibold text-white">What it does</h2>
              <ul className="mt-4 space-y-3">
                {agent.bullets.map((bullet) => (
                  <li key={bullet} className="flex items-start gap-3">
                    <svg className="mt-1 h-5 w-5 flex-shrink-0 text-[#3dd9d9]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-zinc-200">{bullet}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Architecture */}
            <div className="mt-8">
              <h2 className="text-xl font-semibold text-white">Architecture</h2>
              <p className="mt-3 rounded-lg border border-zinc-700 bg-zinc-800/30 px-4 py-3 font-mono text-sm text-zinc-200">
                {agent.architecture}
              </p>
            </div>

            {/* Actions */}
            <div className="mt-8 flex flex-wrap gap-4">
              {isLive ? (
                <a
                  href={agent.demoUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-xl bg-[#3dd9d9] px-6 py-3 text-sm font-semibold text-[#1a1f2e] transition-all hover:bg-[#2bc4c4] hover:shadow-lg hover:shadow-[#3dd9d9]/25 active:scale-[0.98]"
                >
                  Launch Demo
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              ) : (
                <span className="inline-flex items-center gap-2 rounded-xl border border-zinc-600 px-6 py-3 text-sm text-zinc-400">
                  <span className="h-2 w-2 animate-pulse rounded-full bg-yellow-500"></span>
                  Demo deploying
                </span>
              )}
              <Link
                href="/projects#contact"
                className="inline-flex items-center gap-2 rounded-xl border border-zinc-600 px-6 py-3 text-sm font-semibold text-white transition-all hover:border-[#3dd9d9] hover:text-[#3dd9d9] active:scale-[0.98]"
              >
                Get in Touch
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
