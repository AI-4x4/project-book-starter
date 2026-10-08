import json
import unittest
from farshmaster.core import CATEGORIES, assemble, ingest_raw, load_jsonl


def line(id, text, category=None, **kwargs):
    item = {'id': id, 'source': 'fictional conversation', 'text': text, **kwargs}
    if category is not None:
        item['category'] = category
    return json.dumps(item, ensure_ascii=False)


class TwoPassTests(unittest.TestCase):
    def test_categories_and_candidate_keep_origins(self):
        fragments = load_jsonl('\n'.join([line('A', 'Reach every neighbour', 'intention', scope='project'),
                                          line('B', 'Not everybody has a phone', 'constraint'),
                                          line('C', 'Ask who received notices', 'question')]))
        output = assemble(fragments)
        self.assertEqual(len(CATEGORIES), 12)
        self.assertEqual(output['protoidea_candidate'][0]['fragment_ids'], ['A'])
        self.assertEqual(output['categories']['constraint'][0]['source'], 'fictional conversation')
        self.assertEqual(output['status'], 'CANDIDATE_NOT_CANON')
        self.assertEqual(output['owner_validation'], 'PENDING')
        self.assertEqual(output['discarded_fragment_ids'], [])

    def test_unlabelled_input_remains_unknown_not_guessed(self):
        out = assemble(load_jsonl(line('X', 'We might use email')))
        self.assertEqual(out['gaps'], ['X'])
        self.assertFalse(out['protoidea_candidate'])

    def test_narrow_auto_label_is_candidate_not_decision(self):
        out = assemble(load_jsonl(line('G', 'Хочу, чтобы объявления доходили до всех')))
        item = out['categories']['intention'][0]
        self.assertEqual(item['classification_method'], 'HEURISTIC_CANDIDATE')
        self.assertEqual(out['owner_validation'], 'PENDING')

    def test_explicit_conflict_retained_not_resolved(self):
        text = '\n'.join([line('A', 'Paper only', 'constraint', contradicts=['B']),
                          line('B', 'Digital only', 'constraint')])
        out = assemble(load_jsonl(text))
        self.assertEqual(out['declared_conflicts'], [{'from': 'A', 'to': 'B', 'status': 'DECLARED'}])
        self.assertEqual(len(out['categories']['constraint']), 2)

    def test_missing_conflict_target_is_visible(self):
        out = assemble(load_jsonl(line('A', 'Check source', 'unknown', contradicts=['missing'])))
        self.assertEqual(out['declared_conflicts'][0]['status'], 'UNRESOLVED_REFERENCE')

    def test_mixed_raw_preserves_order_and_holds_unknown_scope(self):
        raw = 'Хочу, чтобы Проект Озеро собирал объявления\nКомпания переносит офис\nУ автора другие планы\n?'
        items = ingest_raw(raw, 'synthetic', 'author', ['Проект Озеро'])
        out = assemble(items)
        self.assertEqual(len(items), 4)
        self.assertEqual([i['line'] for i in items], [1, 2, 3, 4])
        self.assertEqual(out['protoidea_candidate'][0]['fragment_ids'], ['synthetic:1'])
        self.assertEqual(out['needs_scope_review'], ['synthetic:2', 'synthetic:3', 'synthetic:4'])
        self.assertEqual(out['discarded_fragment_ids'], [])
        self.assertEqual(items[0]['scope_method'], 'KEYWORD_CANDIDATE')

    def test_raw_without_project_marker_does_not_forge_protoidea(self):
        out = assemble(ingest_raw('Хочу, чтобы было красиво', 'note'))
        self.assertFalse(out['protoidea_candidate'])
        self.assertEqual(out['needs_scope_review'], ['note:1'])

    def test_explicit_other_intention_is_not_project_intent(self):
        items = load_jsonl(line('C', 'Хочу сменить офис', 'intention', scope='company'))
        out = assemble(items)
        self.assertEqual(out['scope_candidates']['company'], ['C'])
        self.assertFalse(out['protoidea_candidate'])

    def test_bad_category_and_duplicate_fail(self):
        with self.assertRaisesRegex(ValueError, 'unsupported category'):
            load_jsonl(line('A', 'foo', 'invented'))
        with self.assertRaisesRegex(ValueError, 'duplicate id'):
            load_jsonl(line('A', 'one') + '\n' + line('A', 'two'))


if __name__ == '__main__':
    unittest.main()
