"""Read-only monitor of a project starter binding. No actions, no scheduling."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def _time(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed.astimezone(timezone.utc) if parsed.tzinfo else None
    except ValueError:
        return None


def inspect(project: Path, now: datetime | None = None):
    project = project.resolve()
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('now must include timezone')
    result = {'project': str(project), 'checked_at': now.isoformat(), 'signals': []}
    signals = result['signals']
    binding = project / 'MONITOR.json'
    if not binding.is_file():
        signals.append({'id': 'binding', 'status': 'UNKNOWN', 'reason': 'MONITOR.json missing'})
        return result
    try:
        config = json.loads(binding.read_text(encoding='utf-8'))
        route = config['route']
        if route not in ('standard', 'complex'):
            raise ValueError('route must be standard or complex')
        ttl = config['max_observation_age_hours']
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)) or not (0 < ttl <= 8760):
            raise ValueError('invalid max_observation_age_hours')
    except (OSError, ValueError, KeyError, TypeError) as error:
        signals.append({'id': 'binding', 'status': 'FAIL', 'reason': f'invalid binding: {error}'})
        return result
    # Structural availability is not semantic health or evidence of adoption.
    required = ['BOUNDARY.md', 'SOURCES.md', 'STATE.md', 'WORK-LOG.md']
    required += ['EXTRACTION.md', 'SPECIFICATION.md'] if route == 'standard' else ['AUTHOR-INTENT.md', 'BOOK.md', 'AMENDMENTS.md', 'TRACE.md']
    for name in required:
        path = project / name
        status = 'OK' if path.is_file() and path.stat().st_size > 0 else 'FAIL'
        signals.append({'id': f'file:{name}', 'status': status, 'reason': 'nonempty file present' if status == 'OK' else 'missing or empty; content not verified'})
    raw = config.get('observation')
    if not isinstance(raw, dict) or not raw:
        signals.append({'id': 'user_outcome', 'status': 'NOT_TESTED', 'reason': 'no observation declared'})
        return result
    observed = _time(raw.get('at'))
    source = raw.get('source')
    if observed is None or not isinstance(source, str) or not source.strip():
        signals.append({'id': 'user_outcome', 'status': 'UNKNOWN', 'reason': 'observation requires timezone-aware at and nonempty source'})
    elif observed > now:
        signals.append({'id': 'user_outcome', 'status': 'UNKNOWN', 'reason': 'observation is in the future'})
    elif (now - observed).total_seconds() > ttl * 3600:
        signals.append({'id': 'user_outcome', 'status': 'STALE', 'reason': 'observation exceeds freshness limit; source not authenticated'})
    else:
        signals.append({'id': 'user_outcome', 'status': 'NOT_TESTED', 'reason': 'fresh declaration only; outcome and independence not verified'})
    return result


def main():
    parser = argparse.ArgumentParser(description='Inspect starter project without changing it')
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.project), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
