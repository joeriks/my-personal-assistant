# Getting started

Create a private copy of this public template before adding personal information. Current tasks, projects, areas, and notes are the source of truth in your repository.

## Prerequisites

Use an authorized GitHub integration with file read/write access, or install Git and the [GitHub CLI](https://cli.github.com/) (`gh`) for local work. With the CLI, verify authentication with:

```powershell
gh auth status
```

You may clone your private repository and work in the local folder, or use an authorized remote connector in Codex when available. A normal clone includes files and Git history, but does not automatically include GitHub Issues or GitHub Projects.

On Windows, if your Python installation lacks time-zone data, install `tzdata` before validation:

```powershell
python -m pip install tzdata
```

## File structure and IDs

Create current records in these directories:

| Type | Path | ID format |
| --- | --- | --- |
| Task | `data/tasks/<id>.json` | `task-<lowercase-slug>` |
| Project | `data/projects/<id>.json` | `project-<lowercase-slug>` |
| Area | `data/areas/<id>.md` | `area-<lowercase-slug>` |
| Note | `data/notes/` | its own stable ID |

Use the templates in `templates/` as starting points. They are examples and must not be placed in active data directories. Required fields and allowed values are documented in `docs/data-model.md` and checked by `scripts/validate.py`; there are no formal JSON schemas. Use UTC with `Z` for timestamps, for example `2026-01-01T12:00:00Z`.

For example, create `data/tasks/task-schedule-appointment.json` with the ID `task-schedule-appointment` in both its filename and `id` field.

## Validate before committing

Run validation from the repository root before sharing changes:

```powershell
python scripts/validate.py
```

Then follow your normal Git routine to review, commit, and push changes.

## Daily activity

A daily log is stored in `data/activity/YYYY-MM-DD.json`. Its date is local to the profile timezone, while `logged_at` is always UTC with `Z`. Record time as `exact`, `approximate`, or `unknown`, and mark entries recorded later as `retrospective`. Never conclude that work was completed solely from an AI-created Git commit.

No automatic tracking or recurring reminder is built yet. Add one only after a real schedule has been decided and installed.

## ChatGPT and Codex

Codex can work in a local clone or through an authorized remote connector. ChatGPT does not automatically read `AGENTS.md`. Start a ChatGPT session with a clear instruction to read `AGENTS.md`, `README.md`, and personal profile settings through the available repository connection. `docs/clients.md` explains access checks and includes a reusable prompt.

## GitHub Issues and Projects

GitHub Issues and Projects can be used as a mirror or workspace, but synchronization is not automatic. A GitHub Project belongs to an account or organization and can be linked to the repository. Personal Projects with a fine-grained token or GitHub App may need account-specific permission checks.

Always preflight actual permissions and access before building an integration. On a future import, compare every external change against a stored last-synced baseline and detect conflicts before overwriting a file. No automated synchronization exists yet.

Calendar OAuth and calendar workflows are also not included yet. Add them later after deciding the need, permissions, and integration path.
