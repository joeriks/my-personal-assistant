# Data model and responsibilities

## One foundation, several views

Files are the durable foundation. Issues and Projects make the information easier to work with. Do not also maintain tasks in separate Markdown lists or duplicate project folders. Notes may link to IDs, but they are not a second task list.

A task has a stable ID regardless of its title. IDs use `task-`, `project-`, or `area-`, followed by lowercase ASCII letters, numbers, and hyphens. Add a new suffix when a name conflicts. A JSON filename must match its ID. An area ID comes from its Markdown filename.

## Task

All fields below are required; optional values use `null` or an empty string as shown. The format follows `templates/task.json`.

| Field | Value |
|---|---|
| `schema_version` | `1` |
| `id` | Stable task ID |
| `title` | Non-empty text |
| `area_id` | Existing area ID or `null` |
| `project_id` | Existing project ID or `null` |
| `status` | `inbox`, `planned`, `in_progress`, `waiting`, `done`, `cancelled` |
| `priority` | `high`, `normal`, `low`; normally `normal` |
| `next_step` | A concrete next step; may be empty in the inbox |
| `description` | Background; may be empty |
| `planned_date` | Planned work date, `YYYY-MM-DD`, or `null` |
| `deadline` | Actual deadline, `YYYY-MM-DD`, or `null` |
| `follow_up_date` | Date to follow up, `YYYY-MM-DD`, or `null` |
| `estimate_minutes` | Positive integer or `null` |
| `updated_at` | Actual most-recent write time, ISO 8601 UTC with `Z` |

## Project

Projects have `schema_version`, `id`, `title`, `area_id`, `status`, `outcome`, and `updated_at`. Status is `active`, `paused`, `done`, or `cancelled`. `outcome` describes the intended result and may remain empty until it is clear. A project does not need a deadline; extend the format when that becomes necessary.

Tasks reference a project ID. A project must not contain a parallel copy of its task list.

## Profile and areas

`personal/profile.json` has `schema_version: 1`, `name` (text or `null`), `timezone` (an IANA zone), and `language` (a language code). The profile is excluded from exports; `templates/profile.json` provides a generic example.

Areas are Markdown files named `area-<slug>.md`; their text describes an ongoing responsibility and desired state. Notes are Markdown files with dates and references to stable IDs. The user's private routines belong in `personal/preferences.md`.

## Activity log

`data/activity/YYYY-MM-DD.json` contains `schema_version: 1`, `date`, `timezone`, and an `entries` list. The date is the local activity day. Each entry has `id` (`activity-<slug>`), `description` (non-empty text), `task_id` and `project_id` (existing IDs or `null`), `started_at` and `ended_at` (UTC with `Z` or `null`), `time_precision` (`exact`, `approximate`, `unknown`), `mode` (`contemporaneous`, `retrospective`), `logged_at` (the actual UTC time it was recorded), and `outcome` (text, which may be empty).

An unknown time must be `null`; an end time requires a start time and cannot precede it. Known or approximate start times must belong to the file's local date. The same activity ID cannot appear on two days. Retrospective logging is allowed, but uncertain times must not be presented as exact. An activity may have no task link and does not automatically prove that a task is complete.

## GitHub connection

An Issue receives the hidden marker `<!-- assistant:id=<stable-id> -->`. Areas and projects may be represented by labels according to `config/labels.json`. Board fields are defined in `config/project.json`. Project status is different from task status.

Important GitHub comments and decisions must be summarized in the relevant files when needed for reconstruction; original comments may remain in GitHub. Attachments needed for reconstruction require an explicit storage solution; a private Issue link is not a local copy.

When synchronization is introduced, store object mappings and last-synchronized field values in `personal/github-sync.json`. A three-way comparison of file, GitHub, and baseline prevents overwriting a newer change. Timestamps alone do not resolve conflicts. Update the baseline only after both sides have been read back and match.

Synchronization is not automated yet. The first connection must inventory GitHub, check access, and reconcile any differences.

## Validation

`scripts/validate.py` validates the profile, configuration, generic JSON examples, and real tasks and projects, including IDs, dates, and references. It cannot validate the meaning of Markdown text. A calendar format is not defined yet, so do not store real calendar data until there is a format and validation.
