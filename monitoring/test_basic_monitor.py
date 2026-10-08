import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from monitoring.basic_monitor import inspect

NOW = datetime(2026, 10, 6, 0, 0, tzinfo=timezone.utc)


class BasicMonitorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def bind(self, route='standard', observation=None):
        doc = {'route': route, 'max_observation_age_hours': 24}
        if observation is not None:
            doc['observation'] = observation
        (self.root / 'MONITOR.json').write_text(json.dumps(doc))

    def signal(self, identifier):
        return next(s for s in inspect(self.root, NOW)['signals'] if s['id'] == identifier)

    def test_no_binding_is_unknown(self):
        self.assertEqual(self.signal('binding')['status'], 'UNKNOWN')

    def test_missing_document_is_fail_but_outcome_not_tested(self):
        self.bind()
        self.assertEqual(self.signal('file:STATE.md')['status'], 'FAIL')
        self.assertEqual(self.signal('user_outcome')['status'], 'NOT_TESTED')

    def test_fresh_declaration_is_not_verified_success(self):
        self.bind(observation={'at': '2026-10-05T23:00:00Z', 'source': 'manual report'})
        self.assertEqual(self.signal('user_outcome')['status'], 'NOT_TESTED')

    def test_stale_observation(self):
        self.bind(observation={'at': '2026-10-01T00:00:00Z', 'source': 'manual report'})
        self.assertEqual(self.signal('user_outcome')['status'], 'STALE')

    def test_no_source_is_unknown(self):
        self.bind(observation={'at': '2026-10-05T23:00:00Z', 'source': ''})
        self.assertEqual(self.signal('user_outcome')['status'], 'UNKNOWN')

    def test_complex_requires_book(self):
        self.bind(route='complex')
        self.assertEqual(self.signal('file:BOOK.md')['status'], 'FAIL')
        self.assertFalse(any(s['id'] == 'file:SPECIFICATION.md' for s in inspect(self.root, NOW)['signals']))

    def test_invalid_binding_fails_without_claiming_health(self):
        self.bind(route='elsewhere')
        self.assertEqual(self.signal('binding')['status'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
