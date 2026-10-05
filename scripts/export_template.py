"""Export only explicitly selected generic files; never copy repository history."""
import argparse
import json
import shutil
from pathlib import Path

GENERIC_FILES = (
    'README.md', 'AGENTS.md', '.gitignore',
    'config/labels.json', 'config/project.json',
    'docs/getting-started.md', 'docs/sharing.md', 'docs/data-model.md', 'docs/clients.md',
    'templates/task.json', 'templates/project.json', 'templates/profile.json',
    'templates/area.md', 'templates/note.md', 'templates/activity.json',
    'scripts/validate.py', 'scripts/export_template.py',
    '.github/ISSUE_TEMPLATE/task.yml', '.github/ISSUE_TEMPLATE/project.yml',
    '.github/ISSUE_TEMPLATE/config.yml', '.github/workflows/validate.yml',
)


def export(root, output):
    root, output = root.resolve(), output.resolve()
    if output == root or root in output.parents or output in root.parents:
        raise ValueError('Output must be outside the source repository, not an ancestor.')
    if output.exists():
        raise ValueError('Output directory must not exist; choose a new directory.')
    sources = []
    for name in GENERIC_FILES:
        source = root / name
        if not source.is_file() or source.resolve() != source.absolute():
            raise ValueError(f'Missing or symbolic-link source: {name}')
        sources.append((name, source))
    # Preflight completes before the output directory or any files are written.
    output.mkdir(parents=True, exist_ok=False)
    for name, source in sources:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    # Only freshly generated empty personal directories, never copied contents.
    for folder in ('areas', 'projects', 'tasks', 'notes', 'activity', 'calendar'):
        target = output/'data'/folder
        target.mkdir(parents=True)
        (target/'README.md').write_text('# Empty personal directory\n\nAdd real information only in your private installation. See docs/data-model.md for the format.\n', encoding='utf-8')
    (output/'data/README.md').write_text('# My notebook\n\nUse the areas, projects, tasks, notes, activity, and calendar folders in your private copy.\n', encoding='utf-8')
    (output/'personal').mkdir()
    profile = json.loads((root/'templates/profile.json').read_text(encoding='utf-8-sig'))
    (output/'personal/profile.json').write_text(json.dumps(profile, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (output/'personal/preferences.md').write_text('# My preferences\n\nFill this in with the assistant in your own private installation.\n', encoding='utf-8')
    (output/'personal/README.md').write_text('# Personal information\n\nProfile, preferences, and integration mappings are private and excluded from exports. Never store credentials here.\n', encoding='utf-8')
    return len(sources)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        count = export(Path(__file__).resolve().parents[1], args.output)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Export refused: {exc}\n')
    print(f'Exported {count} generic files plus fresh empty personal structure to {args.output.resolve()}')
    print('Review EVERY exported file for personal content before publishing. No Git history, Issues or Projects copied.')
