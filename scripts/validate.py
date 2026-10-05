"""Validate the personal assistant file format using Python's standard library."""
import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

TASK_FIELDS = set('schema_version id title area_id project_id status priority next_step description planned_date deadline follow_up_date estimate_minutes updated_at'.split())
PROJECT_FIELDS = set('schema_version id title area_id status outcome updated_at'.split())
ACTIVITY_FIELDS = set('schema_version date timezone entries'.split())
ENTRY_FIELDS = set('id description task_id project_id started_at ended_at time_precision mode logged_at outcome'.split())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=pairs)


def fields(obj, expected):
    require(isinstance(obj, dict), 'Expected a JSON object')
    require(set(obj) == expected, f'Missing fields: {sorted(expected-set(obj))}; unknown fields: {sorted(set(obj)-expected)}')


def text(value, name, nonempty=False):
    require(isinstance(value, str) and (not nonempty or bool(value.strip())), f'{name}: expected text')


def identifier(value, prefix):
    require(isinstance(value, str) and bool(re.fullmatch(prefix + r'-[a-z0-9]+(?:-[a-z0-9]+)*', value)), f'Invalid {prefix} ID: {value!r}')


def day(value):
    require(isinstance(value, str) and bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', value)), 'Expected YYYY-MM-DD')
    date.fromisoformat(value)


def instant(value):
    require(isinstance(value, str) and value.endswith('Z'), 'Expected a UTC timestamp ending in Z')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require('T' in value and parsed.utcoffset().total_seconds() == 0, 'Expected an ISO 8601 UTC timestamp')
    return parsed


def version(obj):
    require(type(obj['schema_version']) is int and obj['schema_version'] == 1, 'schema_version must be 1')


def timezone(value):
    text(value, 'timezone', True)
    try:
        ZoneInfo(value)
    except ZoneInfoNotFoundError as exc:
        raise ValueError('Unknown timezone; install tzdata on Windows if required') from exc


def entity(obj, kind, path=None):
    fields(obj, TASK_FIELDS if kind == 'task' else PROJECT_FIELDS)
    version(obj)
    identifier(obj['id'], kind)
    if path:
        require(path.stem == obj['id'], 'Filename must match id')
    text(obj['title'], 'title', True)
    if obj['area_id'] is not None:
        identifier(obj['area_id'], 'area')
    instant(obj['updated_at'])
    if kind == 'project':
        require(obj['status'] in ('active', 'paused', 'done', 'cancelled'), 'Invalid project status')
        text(obj['outcome'], 'outcome')
        return
    if obj['project_id'] is not None:
        identifier(obj['project_id'], 'project')
    require(obj['status'] in ('inbox', 'planned', 'in_progress', 'waiting', 'done', 'cancelled'), 'Invalid task status')
    require(obj['priority'] in ('high', 'normal', 'low'), 'Invalid priority')
    for key in ('next_step', 'description'):
        text(obj[key], key)
    for key in ('planned_date', 'deadline', 'follow_up_date'):
        if obj[key] is not None:
            day(obj[key])
    value = obj['estimate_minutes']
    require(value is None or (type(value) is int and value > 0), 'estimate_minutes must be a positive integer or null')


def profile(obj):
    fields(obj, set('schema_version name timezone language'.split()))
    version(obj)
    if obj['name'] is not None:
        text(obj['name'], 'name', True)
    timezone(obj['timezone'])
    text(obj['language'], 'language', True)


def activity(obj, path=None):
    fields(obj, ACTIVITY_FIELDS)
    version(obj)
    day(obj['date'])
    timezone(obj['timezone'])
    if path:
        require(path.stem == obj['date'], 'Activity filename must match date')
    require(isinstance(obj['entries'], list), 'entries must be an array')
    seen = set()
    for entry in obj['entries']:
        fields(entry, ENTRY_FIELDS)
        identifier(entry['id'], 'activity')
        require(entry['id'] not in seen, 'Duplicate activity ID')
        seen.add(entry['id'])
        text(entry['description'], 'description', True)
        text(entry['outcome'], 'outcome')
        for key, prefix in (('task_id', 'task'), ('project_id', 'project')):
            if entry[key] is not None:
                identifier(entry[key], prefix)
        require(entry['time_precision'] in ('exact', 'approximate', 'unknown'), 'Invalid time_precision')
        require(entry['mode'] in ('contemporaneous', 'retrospective'), 'Invalid logging mode')
        instant(entry['logged_at'])
        start = instant(entry['started_at']) if entry['started_at'] is not None else None
        end = instant(entry['ended_at']) if entry['ended_at'] is not None else None
        require(end is None or start is not None, 'ended_at requires started_at')
        require(start is None or end is None or end >= start, 'Activity ends before it starts')
        if entry['time_precision'] == 'unknown':
            require(start is None and end is None, 'Unknown times must be null')
        else:
            require(start is not None, 'Known/approximate times need started_at')
        if start is not None:
            require(start.astimezone(ZoneInfo(obj['timezone'])).date().isoformat() == obj['date'], 'Activity belongs to its local start date')
    return obj['entries']


def validate(root):
    errors, tasks, projects, entries = [], {}, {}, []
    def check(path, operation):
        try:
            return operation(load(path))
        except (ValueError, TypeError, KeyError, OSError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
            return None
    check(root/'personal/profile.json', profile)
    check(root/'templates/profile.json', profile)
    check(root/'templates/task.json', lambda obj: entity(obj, 'task'))
    check(root/'templates/project.json', lambda obj: entity(obj, 'project'))
    check(root/'templates/activity.json', activity)
    areas = set()
    for path in (root/'data/areas').glob('*.md'):
        if path.name == 'README.md':
            continue
        try:
            identifier(path.stem, 'area')
            areas.add(path.stem)
        except ValueError as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    for kind, collection in (('task', tasks), ('project', projects)):
        for path in (root/f'data/{kind}s').glob('*.json'):
            def read(obj, path=path, kind=kind):
                entity(obj, kind, path)
                return obj
            obj = check(path, read)
            if obj:
                collection[obj['id']] = obj
    for obj in [*tasks.values(), *projects.values()]:
        if obj['area_id'] is not None and obj['area_id'] not in areas:
            errors.append(f"{obj['id']}: missing area {obj['area_id']}")
        if obj.get('project_id') is not None and obj['project_id'] not in projects:
            errors.append(f"{obj['id']}: missing project {obj['project_id']}")
    all_activity_ids = set()
    for path in (root/'data/activity').glob('*.json'):
        current = check(path, lambda obj, path=path: activity(obj, path))
        for entry in current or []:
            if entry['id'] in all_activity_ids:
                errors.append(f"{entry['id']}: duplicate ID across daily logs")
            all_activity_ids.add(entry['id'])
            for key, collection in (('task_id', tasks), ('project_id', projects)):
                if entry[key] is not None and entry[key] not in collection:
                    errors.append(f"{entry['id']}: missing reference {entry[key]}")
            entries.append(entry)
    for path in (root/'data/calendar').iterdir():
        if path.name != 'README.md':
            errors.append(f'{path.relative_to(root)}: calendar format not implemented yet')
    for filename in ('labels.json', 'project.json'):
        def config(obj):
            require(isinstance(obj, dict), 'Expected config object')
            version(obj)
            if filename == 'labels.json':
                require(isinstance(obj.get('labels'), list), 'labels must be an array')
                names = set()
                for label in obj['labels']:
                    text(label['name'], 'label name', True)
                    require(label['name'] not in names, 'Duplicate label')
                    names.add(label['name'])
                    require(bool(re.fullmatch('[0-9a-fA-F]{6}', label['color'])), 'Invalid label color')
            else:
                text(obj['title'], 'project title', True)
                require(isinstance(obj.get('fields'), list) and isinstance(obj.get('views'), list), 'fields/views must be arrays')
                status = next(field for field in obj['fields'] if field['name'] == 'Status')
                require(set(status['mapping']) == {'inbox','planned','in_progress','waiting','done','cancelled'}, 'Status mapping incomplete')
        try:
            check(root/'config'/filename, config)
        except StopIteration:
            errors.append('config/project.json: Status field missing')
    return errors, (len(tasks), len(projects), len(entries))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    problems, counts = validate(args.root.resolve())
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print(f'OK: {counts[0]} tasks, {counts[1]} projects, {counts[2]} activity entries; templates and configuration validated.')
