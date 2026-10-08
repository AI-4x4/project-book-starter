"""Offline structural smoke check; does not certify meaning or authority."""
from pathlib import Path
import re
import sys
root = Path(__file__).resolve().parents[1]
required = ["README.md", "README.ru.md", "RELEASE-REVIEW.md", "RELEASE-NOTES.md", "RELEASE-NOTES.ru.md", "docs/QUICKSTART.md", "docs/QUICKSTART.ru.md", "docs/STATUS.md", "docs/STATUS.ru.md", "farshmaster/README.ru.md", "docs/PROCESS.md", "docs/DECISIONS-AND-CHANGES.md", "docs/EXTENSIONS.md", "templates/common/BOUNDARY.md", "templates/common/SOURCES.md", "templates/common/STATE.md", "templates/common/WORK-LOG.md", "templates/standard/EXTRACTION.md", "templates/standard/SPECIFICATION.md", "templates/complex/AUTHOR-INTENT.md", "templates/complex/BOOK.md", "templates/complex/AMENDMENTS.md", "templates/complex/TRACE.md", "examples/fictional-app/README.md", "farshmaster/README.md", "farshmaster/core.py", "monitoring/README.md", "monitoring/basic_monitor.py", "templates/common/MONITOR.json"]
invalid = [p for p in required if not (root / p).is_file() or not (root / p).read_text(encoding="utf-8").strip()]
if invalid:
    print("FAIL, missing/empty:", ", ".join(invalid)); sys.exit(1)
# The default English landing page and Russian landing page must each expose both choices.
pairs = [("README.md", "README.ru.md"),
         ("farshmaster/README.md", "farshmaster/README.ru.md"),
         ("docs/QUICKSTART.md", "docs/QUICKSTART.ru.md"),
         ("docs/STATUS.md", "docs/STATUS.ru.md"),
         ("RELEASE-NOTES.md", "RELEASE-NOTES.ru.md")]
for english, russian in pairs:
    for name in (english, russian):
        page = root / name
        links = re.findall(r"\]\(([^)]+)\)", page.read_text(encoding="utf-8"))
        for target in (Path(english).name, Path(russian).name):
            if target not in links:
                print(f"FAIL, language switch missing in {name}: {target}"); sys.exit(1)
        for target in links:
            if not target.startswith(("http://", "https://", "#", "/")) and not (page.parent / target.split("#")[0]).is_file():
                print(f"FAIL, broken local link in {name}: {target}"); sys.exit(1)
print(f"PASS: {len(required)} nonempty files and {len(pairs)} language pairs; semantic validity, permissions and real-world effects NOT CHECKED")
