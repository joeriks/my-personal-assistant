# What I did

Keep one daily log in `YYYY-MM-DD.json`, using `templates/activity.json`. The date is the person's local activity day in their profile timezone. For work across midnight, use the start date or split into two entries when useful.

Add entries when the person reports an activity, or reconstruct the day together later. Activities do not need task/project links. Time spent and task completion are different things.

Preserve uncertainty: `time_precision: unknown` and null times when unknown, `approximate` for estimates, or `exact` for known times. `mode` identifies recording during the activity (`contemporaneous`) or later (`retrospective`). `logged_at` is the actual recording time.

No automatic tracking, background monitoring, or recurring reminders are installed. The assistant can offer check-ins during an active conversation and help review the day when asked.
