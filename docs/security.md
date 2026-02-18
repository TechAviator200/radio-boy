# Security Policy — Radio Boy

## Scope

Radio Boy is a **portfolio / demo** project — a single-user AI music agent.
It is **not** a production SaaS application. The controls below are proportional
to that scope while demonstrating security-aware engineering practices.

---

## Threat Model & Trust Boundaries

| Boundary | Trusted | Untrusted |
|---|---|---|
| User chat input | — | User-supplied text sent to the LLM |
| System prompts | Backend-controlled prompts | — |
| OpenAI API | — | Responses from the LLM (treat as untrusted content) |
| Deezer / music APIs | — | Third-party API responses |
| Frontend → Backend | Same-origin or CORS-allowed | Everything else |

**Key risks:**
- **Prompt injection** — malicious user input could attempt to override system
  prompts. Mitigated by keeping system prompts server-side and not reflecting
  raw LLM output into privileged contexts.
- **SSRF / open redirect** — the backend makes outbound HTTP calls (Deezer,
  OpenAI). URLs are constructed from known API bases, not from user input.
- **Credential leakage** — API keys stored in `.env` files that are gitignored
  and never committed.

---

## Secrets Handling

| Rule | Detail |
|---|---|
| Storage | All secrets are environment variables loaded via `python-dotenv` |
| Version control | `.env` and credential files are in `.gitignore` |
| CI/CD | Use GitHub Actions secrets or your deployment platform's secret manager |
| Rotation | Rotate OpenAI / Deezer keys if you suspect compromise |

**Never commit** `.env`, `*token*.json`, or `credentials/` to the repository.

---

## Automated Security Checks

| Check | Tool | Workflow |
|---|---|---|
| Secret scanning | [gitleaks](https://github.com/gitleaks/gitleaks) | `security.yml` |
| Python dependency audit | [pip-audit](https://github.com/pypa/pip-audit) | `security.yml` |
| Python SAST | [bandit](https://github.com/PyCQA/bandit) | `security.yml` |
| JS/TS dependency audit | `npm audit` | `security.yml` (when frontend is tracked) |
| Deep code analysis | [CodeQL](https://codeql.github.com/) | `codeql.yml` |
| Dependency updates | [Dependabot](https://docs.github.com/en/code-security/dependabot) | `dependabot.yml` |

---

## Outbound-Risk Safeguards

- The backend only calls known API endpoints (OpenAI, Deezer).
- CORS is restricted to specific origins in `radio_boy_app.py`.
- No user-supplied URLs are followed by the backend.
- For a production deployment, add rate limiting (e.g., `slowapi`) and
  structured request logging.

---

## Out of Scope (Demo Repo)

The following are **not** implemented because this is a single-user demo:

- Multi-user authentication (OAuth / SSO)
- Role-based access control (RBAC)
- Multi-tenant data isolation
- Compliance frameworks (SOC 2, GDPR)
- WAF / DDoS protection
- Audit log persistence

---

## Production Hardening Path

If Radio Boy were promoted to a production service, the following would be needed:

1. **Authentication & authorization** — OAuth 2.0 / SSO, RBAC per endpoint
2. **Rate limiting** — per-user and per-IP request caps
3. **Audit logging** — structured logs shipped to a SIEM or observability stack
4. **Per-tenant isolation** — separate data stores or row-level security
5. **Input validation** — schema validation on all API inputs (Pydantic models)
6. **Observability** — distributed tracing, error tracking, uptime monitoring
7. **Infrastructure** — TLS everywhere, private networking, secret manager (Vault / AWS SM)
8. **Dependency policy** — automated merge of patch-level Dependabot PRs, manual review for minor/major
