# Security Review — Task Tracker

**Status:** Draft based on code discussed during development. This still needs the real Module 5
prompts (5.2A, 5.2B, 5.2C) run against the live repo in Codex App — findings here are a starting
point, not a substitute for that read-only audit and a manual scan.

| ID | Severity | File / location | Finding | Evidence | Suggested next step | Confidence |
|----|----------|------------------|---------|----------|----------------------|------------|
| 1 | Medium | `app/main.py` | No authentication or authorization on any endpoint | All routes (`POST/GET/PATCH/DELETE /tasks`) are open | Confirm this is an intentional course-scope decision; document it explicitly | Medium |
| 2 | Medium | `app/main.py` (CORS middleware) | `allow_origins=["*"]` permits any origin to call the API | Added to unblock the local frontend | Restrict to actual local frontend origin(s) before treating this as anything beyond local dev | High |
| 3 | Low | `app/storage.py` | In-memory dict storage — no persistence, no concurrency control | `_tasks: dict[str, TaskResponse] = {}` | Acceptable for course scope; note as a known limitation, not a bug | High |
| 4 | Low | `app/main.py` route handlers | Error responses use FastAPI's default `HTTPException` detail strings | e.g. `f"Task with id {task_id} not found"` | Low risk — no stack traces or internals exposed to the client | High |
| 5 | Low | `requirements.txt` | Dependency versions pinned, but no automated vulnerability scanning configured | No Dependabot/CI security scan present | Optional: add a dependency audit step to CI later | Medium |
| 6 | Low | `frontend/index.html` | Task text is escaped via `escapeHtml()` before DOM insertion | Confirmed present in `createCardElement` | Good practice already in place — no action needed | High |

## Files inspected
`app/main.py`, `app/storage.py`, `app/models.py`, `app/business_rules.py`, `frontend/index.html`,
`requirements.txt`.

## Categories with no issue found
- Input validation on request bodies (handled by Pydantic models with `extra="forbid"`)
- SQL injection (not applicable — no database)
- Secrets in code (none observed)

## Assumptions / limits of this audit
- This draft was generated from code reviewed during development, not a fresh live read of the
  repository via Codex App. Re-run prompt 5.2A against the actual repo and reconcile any
  differences before treating this as final.
- Docker and CI files have not yet had their own security pass — worth a second look once they
  exist in the repo.