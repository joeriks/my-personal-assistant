# Share a clean template

You can export a reusable, empty template from a personal repository. The export must contain only approved structural and example files, never personal data or Git history.

Run this from the repository root and choose a new destination directory that does not already exist:

```powershell
python scripts/export_template.py --output C:\path\to\a-new-empty-directory
```

The script uses a safe allowlist. It does not copy `.git` or private data. Review the exported files before sharing, especially after adding files or folders since the last export. An allowlisted path is not sufficient evidence that its contents are generic.

Create a new public repository from the exported directory, initialize fresh Git history there, and publish only after the allowlist review is complete. Never publish the personal working repository or its history, which may contain earlier personal information.

Files in `templates/` must remain generic. Keep personal names, real tasks, projects, notes, and authentication information only in the private working copy.
