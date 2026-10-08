# Project Book Starter v0.1.0 — preview

A bounded first release: Project Book and conventional-specification templates, mixed-text intake via Farshmaster, basic local monitoring, a synthetic example and runnable instructions. [Русская версия](RELEASE-NOTES.ru.md).

Requires Python 3.10+. No external dependencies, network calls, service startup or model integration.

Local checks passed: package structure, 9 basic Farshmaster tests, 7 basic monitoring tests, and both CLIs on synthetic inputs. `RELEASE-MANIFEST.json` records the exact file bytes of the *original published v0.1.0 preview*, not later documentation revisions.

Principal limit: Farshmaster uses lines and narrow heuristics. It cannot reliably understand arbitrary text, approve an author's intent or edit a Project Book. The monitor does not attest useful outcomes. The full loop has not been tested on a real project; this is a preview, not a proven technology.

The package contains generic templates and fictional examples, not private conversations, infrastructure, other projects' Books or internal-repository history. Documentation corrections after the frozen preview require a separately reviewed release manifest before a new version is claimed.
