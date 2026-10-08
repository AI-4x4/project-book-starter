"""Offline structural smoke check; does not certify meaning or authority."""
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
required = ["README.md", "README.ru.md", "RELEASE-REVIEW.md", "docs/PROCESS.md", "docs/DECISIONS-AND-CHANGES.md", "docs/EXTENSIONS.md", "templates/common/BOUNDARY.md", "templates/common/SOURCES.md", "templates/common/STATE.md", "templates/common/WORK-LOG.md", "templates/standard/EXTRACTION.md", "templates/standard/SPECIFICATION.md", "templates/complex/AUTHOR-INTENT.md", "templates/complex/BOOK.md", "templates/complex/AMENDMENTS.md", "templates/complex/TRACE.md", "examples/fictional-app/README.md", "farshmaster/README.md", "farshmaster/core.py", "monitoring/README.md", "monitoring/basic_monitor.py", "templates/common/MONITOR.json"]
invalid = [p for p in required if not (root / p).is_file() or not (root / p).read_text(encoding="utf-8").strip()]
if invalid:
    print("FAIL, missing/empty:", ", ".join(invalid)); sys.exit(1)
print(f"PASS: {len(required)} nonempty files; semantic validity, permissions and real-world effects NOT CHECKED")
