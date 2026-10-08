"""Bounded two-pass intake: classify supplied fragments, then assemble a review candidate.

No LLM calls, no inference of authorship/meaning, no write to a Project Book.
"""
import argparse
import json
import hashlib
from pathlib import Path

# Illustrative categories from an early discussion, not an owner-approved ontology.
SCOPES = ('project', 'author', 'company', 'environment', 'other', 'unknown')

CATEGORIES = (
    'intention', 'desired_result', 'problem', 'example', 'fact', 'assumption',
    'preference', 'constraint', 'decision', 'question', 'contradiction', 'unknown',
)


def suggest_category(text):
    """Very narrow candidate routing, never a semantic fact or approved label."""
    value = text.strip().lower()
    matches = []
    if value.startswith(('хочу, чтобы ', 'цель: ', 'i want ', 'we want ')):
        matches.append('intention')
    if value.startswith(('результат: ', 'desired result: ')):
        matches.append('desired_result')
    if value.startswith(('проблема: ', 'problem: ')):
        matches.append('problem')
    if value.startswith(('например: ', 'example: ')):
        matches.append('example')
    if value.startswith(('предполагаю, что ', 'допущение: ', 'assumption: ')):
        matches.append('assumption')
    if value.startswith(('нельзя ', 'ограничение: ', 'constraint: ')):
        matches.append('constraint')
    if value.startswith(('вопрос: ', 'question: ')) or value.endswith('?'):
        matches.append('question')
    return matches[0] if len(set(matches)) == 1 else 'unknown'


def ingest_raw(text, source_id, source_role='unknown', project_terms=()):
    """Keep a mixed text's ordered nonempty lines with exact source positions.

    A keyword match is only a candidate relation to the project; nonmatches
    remain unknown rather than being declared irrelevant or thrown away.
    """
    if not isinstance(source_id, str) or not source_id.strip():
        raise ValueError('source_id required')
    if source_role not in ('author', 'additional_material', 'unknown'):
        raise ValueError('unsupported source_role')
    if not isinstance(text, str) or not text.strip():
        raise ValueError('empty raw material')
    terms = [term.strip().casefold() for term in project_terms if term.strip()]
    fragments = []
    for number, raw_line in enumerate(text.splitlines(), 1):
        if not raw_line.strip():
            continue
        category = suggest_category(raw_line)
        project_match = any(term in raw_line.casefold() for term in terms)
        fragments.append({
            'id': f'{source_id}:{number}', 'source': source_id,
            'source_role': source_role, 'line': number, 'text': raw_line,
            'raw_sha256': hashlib.sha256(raw_line.encode('utf-8')).hexdigest(),
            'category': category,
            'classification_method': 'HEURISTIC_CANDIDATE' if category != 'unknown' else 'UNKNOWN',
            'scope': 'project' if project_match else 'unknown',
            'scope_method': 'KEYWORD_CANDIDATE' if project_match else 'UNKNOWN',
            'contradicts': [],
        })
    return fragments


def load_jsonl(text):
    """Parse newline-delimited, individually attributed raw fragments."""
    fragments, ids = [], set()
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'line {line_no}: invalid JSON: {exc.msg}') from exc
        if not isinstance(item, dict):
            raise ValueError(f'line {line_no}: expected object')
        for key in ('id', 'source', 'text'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'line {line_no}: missing nonempty {key}')
        if item['id'] in ids:
            raise ValueError(f'line {line_no}: duplicate id {item["id"]}')
        ids.add(item['id'])
        explicit = 'category' in item
        category = item['category'] if explicit else suggest_category(item['text'])
        if category not in CATEGORIES:
            raise ValueError(f'line {line_no}: unsupported category {category!r}')
        if 'contradicts' in item and (not isinstance(item['contradicts'], list) or
                                      any(not isinstance(ref, str) for ref in item['contradicts'])):
            raise ValueError(f'line {line_no}: contradicts must be a list of IDs')
        scope = item.get('scope', 'unknown')
        if scope not in SCOPES:
            raise ValueError(f'line {line_no}: unsupported scope {scope!r}')
        fragments.append({key: item[key] for key in ('id', 'source', 'text')} |
                         {'category': category, 'classification_method': 'SUPPLIED' if explicit else ('HEURISTIC_CANDIDATE' if category != 'unknown' else 'UNKNOWN'),
                          'scope': scope, 'scope_method': 'SUPPLIED' if 'scope' in item else 'UNKNOWN',
                          'contradicts': item.get('contradicts', [])})
    if not fragments:
        raise ValueError('no input fragments')
    return fragments


def assemble(fragments):
    """Two passes: retain attributed categories; compose a *reviewable*, not accepted, picture."""
    buckets = {category: [] for category in CATEGORIES}
    by_id = {item['id']: item for item in fragments}
    if len(by_id) != len(fragments):
        raise ValueError('duplicate fragment IDs')
    for item in fragments:
        if item['category'] not in buckets:
            raise ValueError('unsupported category')
        buckets[item['category']].append(item)
    scope_buckets = {scope: [] for scope in SCOPES}
    for item in fragments:
        scope = item.get('scope', 'unknown')
        if scope not in scope_buckets:
            raise ValueError('unsupported scope')
        scope_buckets[scope].append(item['id'])
    conflicts = []
    for item in fragments:
        for ref in item['contradicts']:
            conflicts.append({'from': item['id'], 'to': ref,
                              'status': 'DECLARED' if ref in by_id else 'UNRESOLVED_REFERENCE'})
    # The composed overview is an index into exact texts, not a fabricated paraphrase.
    leading = ('intention', 'desired_result', 'problem')
    candidate = [{'category': category, 'fragment_ids': [item['id'] for item in buckets[category] if item.get('scope') == 'project']}
                 for category in leading if any(item.get('scope') == 'project' for item in buckets[category])]
    return {'status': 'CANDIDATE_NOT_CANON', 'owner_validation': 'PENDING',
            'classification_method': 'supplied labels or narrow heuristic candidates; unmatched/ambiguous -> unknown',
            'categories': buckets, 'scope_candidates': scope_buckets,
            'protoidea_candidate': candidate,
            'declared_conflicts': conflicts,
            'gaps': [item['id'] for item in buckets['unknown']],
            'needs_scope_review': scope_buckets['unknown'],
            'assumptions_to_check': [item['id'] for item in buckets['assumption']],
            'discarded_fragment_ids': [],
            'limitations': ['heuristic labels are unverified and may be wrong',
                            'no inference that declared decisions were authorized',
                            'no automatic synthesis of a unified author intent',
                            'a missing keyword does not imply unrelatedness']}


def main():
    parser = argparse.ArgumentParser(description='Two-pass, read-only candidate intake')
    parser.add_argument('input', type=Path, help='permitted raw UTF-8 text or JSONL fragments')
    parser.add_argument('--raw', action='store_true', help='ingest arbitrary text as ordered lines')
    parser.add_argument('--source-id', help='required for --raw; do not use private identifiers in public output')
    parser.add_argument('--source-role', choices=('author', 'additional_material', 'unknown'), default='unknown')
    parser.add_argument('--project-term', action='append', default=[], help='literal marker: candidate project scope, not proof')
    args = parser.parse_args()
    text = args.input.read_text(encoding='utf-8')
    if args.raw:
        fragments = ingest_raw(text, args.source_id, args.source_role, args.project_term)
    else:
        fragments = load_jsonl(text)
    result = assemble(fragments)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
