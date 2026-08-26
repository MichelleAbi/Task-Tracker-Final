# Final AI Review and Ownership Evidence

## AGENTS.md Guardrails

* **Repo-specific stack and commands included:** Yes
* **Docs-first/read-first guardrail included:** Yes
* **Rule for unexpected app/frontend changes included:** Yes

## AI Code Review Mini-Log

| AI Comment                                                                                     | Grade  | Reason                                                                                                   | Verification or Decision                                                                    |
| ---------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Use FastAPI `TestClient` to test API endpoints rather than testing storage functions directly. | Useful | This provides stronger coverage of actual API behavior and aligns better with the project requirements.  | Implemented and confirmed with 6 passing tests.                                             |
| Add validation to prevent invalid task status changes.                                         | Useful | Clear transition rules were required by the project specifications.                                      | Added the validation to the business rules and verified it with tests.                      |
| Add a frontend search bar for tasks.                                                           | Noise  | This was outside the most important backend requirements and would have added unnecessary frontend work. | Not implemented; priority remained on completing and testing the required backend features. |

## AI Security Mini-Review

| Finding                                                                   | File Evidence    | Grade | Reason                                                                                                           | Next Action                                            |
| ------------------------------------------------------------------------- | ---------------- | ----- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Task endpoints do not use authentication or authorization.                | `main.py`        | Valid | This could be a security concern in a real application, but authentication was outside the defined course scope. | Keep it documented as a project limitation.            |
| Tasks are stored only in memory and disappear when the application stops. | `app/storage.py` | Noise | This is an intentional design choice made to keep the project simple and focused on FastAPI concepts.            | No changes needed.                                     |
| Task input is validated before being accepted.                            | `app/models.py`  | Valid | Validation helps prevent invalid or incomplete task data from entering the application.                          | Continue verifying validation through automated tests. |

## Manual Security Check

I manually checked the application's validation behavior, API error handling, status transition rules, and startup configuration.

The main observations were:

* Tasks with missing or blank titles are rejected with HTTP 422.
* Invalid status changes are rejected with HTTP 422.
* Requests for tasks that do not exist return HTTP 404.
* The repository does not contain passwords, API keys, tokens, or other sensitive credentials.

These behaviors were checked through both pytest tests and manual API requests.

## One AI Output I Rejected or Corrected

One AI response suggested that the application already contained rules for controlling task status transitions. After checking the actual implementation and comparing it with the project requirements, I found that this validation had not yet been added.

Instead of accepting the AI's assumption, I implemented the required transition rules myself and added tests to confirm that they worked correctly.

This showed the importance of reviewing AI-generated suggestions against the actual codebase rather than assuming that every AI claim is accurate.

## Three AI Usage Rules

**Never paste:**

* API keys
* Passwords
* Access tokens

**Always verify:**

* AI-generated code before committing it.
* Test results before using them as project evidence.
* Documentation against the actual files and implementation.

**Record AI contributions by:**

* Keeping track of important AI-assisted changes.
* Reviewing, modifying, and testing suggestions before using them.
* Making and documenting the final technical decisions independently.

## Ownership Statement

I confirm that I understand the architecture, implementation, testing, and documentation of this repository and am confident submitting it as my own work. AI tools were used for assistance with planning, debugging, code suggestions, and documentation, but I reviewed, tested, and modified the generated content before using it.

I made the final decisions about the Task Tracker's design and implementation. I understand how the API routes, validation logic, automated tests, CI process, and Docker setup work, and I am able to explain the main decisions behind them. Therefore, I believe the repository accurately reflects my own understanding, learning, and effort.
