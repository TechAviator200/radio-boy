# Radio Boy — AI Music Agent

[![CI](https://github.com/TechAviator200/radio-boy/actions/workflows/ci.yml/badge.svg)](https://github.com/TechAviator200/radio-boy/actions/workflows/ci.yml)
[![Security](https://github.com/TechAviator200/radio-boy/actions/workflows/security.yml/badge.svg)](https://github.com/TechAviator200/radio-boy/actions/workflows/security.yml)
[![CodeQL](https://github.com/TechAviator200/radio-boy/actions/workflows/codeql.yml/badge.svg)](https://github.com/TechAviator200/radio-boy/actions/workflows/codeql.yml)

Radio Boy is an AI-powered music agent that uses OpenAI to generate personalized
music recommendations and streams 30-second previews via the Deezer API. It
demonstrates end-to-end full-stack development with an LLM-driven conversational
interface — built as a portfolio project to showcase AI agent design, API
integration, and modern web development practices.

---

## Architecture

```
┌──────────────┐        ┌──────────────────┐       ┌─────────────┐
│   Frontend   │  HTTP  │     Backend      │  API  │  OpenAI     │
│  (Next.js)   │───────▶│  (FastAPI/Python) │──────▶│  + Deezer   │
└──────────────┘        └──────────────────┘       └─────────────┘
```

| Layer | Tech |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| Backend | Python 3.11, FastAPI, uvicorn |
| AI | OpenAI API (chat completions) |
| Music data | Deezer API (search + 30 s previews) |
| Alt UI | Chainlit chat interface (`backend/chainlit/`) |

---

## Getting Started

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
uvicorn radio_boy_app:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Security Posture & Boundaries

**Current scope:** portfolio / demo — single-user, not a production SaaS.

Automated checks running in CI:

| Check | Tool |
|---|---|
| Secret scanning | gitleaks |
| Python dependency audit | pip-audit |
| Python SAST | bandit |
| JS/TS dependency audit | npm audit |
| Deep code analysis | CodeQL |
| Dependency updates | Dependabot |

For the full threat model, trust boundaries, and production hardening path, see
[docs/security.md](docs/security.md).

---

## Project Structure

```
radio-boy/
├── backend/
│   ├── radio_boy_app.py       # FastAPI main application
│   ├── requirements.txt
│   └── chainlit/              # Alternative Chainlit UI
├── frontend/                  # Next.js frontend
├── radioboy_ui_backup/        # Archived legacy UI (not active)
├── docs/
│   └── security.md
└── .github/
    ├── workflows/
    │   ├── ci.yml
    │   ├── security.yml
    │   └── codeql.yml
    └── dependabot.yml
```

---

## Known Issues

- **Frontend gitlink:** `frontend/` is currently stored as a git commit pointer
  (mode 160000) without a `.gitmodules` file. On a fresh clone the directory
  will be empty. To fix: either register it as a proper submodule or remove
  `frontend/.git` and add the files directly to this repo. The CI frontend job
  is commented out until this is resolved.
