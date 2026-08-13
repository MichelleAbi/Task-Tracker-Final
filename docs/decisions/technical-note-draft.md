# Technical Note: In-Memory Task Storage

**Status:** DRAFT — this must be rewritten in your own words before submission, especially
Trade-offs and Open Questions. This is scaffolding, not the deliverable.

## Context
The Task Tracker needs a persistence layer for task data. The project is scoped as a learning
exercise (Modules 2-4 of an AI-assisted coding course), not a production service.

## Decision
Use an in-memory Python dictionary (`app/storage.py`, `_tasks: dict[str, TaskResponse]`) as the
sole storage mechanism, with no database.

## Alternatives Considered
- **SQLite + SQLModel/SQLAlchemy** — a real embedded database with persistence across restarts.
- **JSON file storage** — writes tasks to a local `.json` file for basic persistence without a
  full database engine.

## Trade-offs
DRAFT - REWRITE IN MY OWN WORDS
- [Add your own reasoning: why in-memory over the alternatives, given the course's learning goals
  vs. what you'd want for a real app]

## Consequences
- Data does not survive a server restart.
- No concurrent-write safety — acceptable at current scale (single learner, local dev) but would
  not hold up under real multi-user load.
- Every automated test relies on a `storage._reset()` fixture to isolate test runs, since there is
  no separate test database to reset instead.

## Open Questions
DRAFT - REWRITE IN MY OWN WORDS
- [Add: at what point would this project need to migrate to SQLite or Postgres?]
- [Add: what would the migration path actually look like given the current `TaskResponse`-shaped
  storage?]

I would do this differently by...