# My Personal Assistant

A reusable notebook for a personal AI assistant. Keep tasks, projects, responsibilities, notes, and a daily activity log in a GitHub repository. Use Codex or ChatGPT to capture information, choose priorities, and pick up where you left off.

**This public repository is a template. Create your own private copy before adding personal information.**

## Get started

1. Create a private repository from this template. The new copy has its own history; Issues and Projects are not copied.
2. Give your AI client access to your repository. A local clone is optional; a GitHub integration with file read/write access can also work.
3. Ask the assistant to read `AGENTS.md`, `README.md`, and your profile and preferences.
4. Tell it what you need help with, one thing at a time.

Example starting prompt:

> Use this repository as my personal assistant notebook. Read AGENTS.md and my profile and preferences first. Help me get started, one question at a time. Check what you can actually read and write, and tell me when something cannot be saved.

See [Getting started](docs/getting-started.md) and [ChatGPT and Codex](docs/clients.md).

## Structure

| Location | Purpose |
|---|---|
| `AGENTS.md` | Instructions for a calm, practical assistant |
| `personal/` | Blank profile and preferences for your private copy |
| `data/areas/` | Ongoing responsibilities |
| `data/projects/` | Projects with a defined outcome |
| `data/tasks/` | Tasks and an unsorted inbox |
| `data/notes/` | Notes, decisions, and conversation summaries |
| `data/activity/` | What you actually did each day, recorded as you go or later |
| `data/calendar/` | Placeholder for an optional calendar integration |
| `config/` | Label and GitHub Project definitions |
| `templates/` | Generic examples, not real personal records |
| `scripts/` | Format validation and allowlisted template export |
| `.github/` | Issue forms and an Actions validation workflow |

## Files first, GitHub views second

Files are the persistent foundation. Issues and Projects provide working views. Stable IDs link tasks to Issues and projects to parent Issues, so the assistant can rebuild views without creating duplicates.

Edits made directly in GitHub must be reconciled with the files. Preserve and resolve conflicting changes instead of silently overwriting them. See the [data model](docs/data-model.md).

The daily activity log records reported work, including activities that did not complete a task. Unknown times remain unknown, estimates are marked, and retrospective entries are identified.

## Check and export

Use Python 3.11 or newer:

```sh
python scripts/validate.py
python scripts/export_template.py --output ../personal-assistant-template
```

Validation uses Python's standard library. Windows may need timezone data: `python -m pip install tzdata`. Actions runs validation on Linux for pushes and pull requests.

Export copies only allowlisted generic files and generates a fresh, empty personal structure. Review all exported content before sharing. See [Sharing a clean template](docs/sharing.md).

## Current scope

This template provides instructions, formats, examples, Issue forms, and validation. It does not automatically create a Project board, synchronize Issues, connect Google Calendar, track activity, or run background reminders. Install and verify those features separately.

Actions can later run prepared jobs for calendar synchronization, summaries, or other bounded processing. It is not a continuous voice server or an exact reminder clock. No API key is needed for this structure.
