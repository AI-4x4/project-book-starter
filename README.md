# Project Book Starter — v0.1.0 preview

A small, experimental starter for turning fragmented project conversations into an authorised, checkable project description. It offers two routes: a conventional specification and a Book-centred route for work with evolving intent. Neither route guarantees a working or well-governed project merely because documents exist.

Requires Python 3.10 or later; uses only the standard library. [Русская версия](README.ru.md). Start with [the runnable walkthrough](docs/QUICKSTART.md) and [the capability status](docs/STATUS.md).

## Start here

1. Agree on the owner, project boundary, allowed source material and intended outcome. Do not paste private conversations into this repository. Keep raw material in a separately controlled location; record references or redacted summaries only when permitted.
2. Create a new project directory **outside this starter**. Copy `templates/common/` and either `templates/standard/` or `templates/complex/`. Replace placeholders with your own decisions. Never edit the common templates as if they were a project's accepted canon.
3. Read `docs/PROCESS.md` and `docs/DECISIONS-AND-CHANGES.md`. State unknowns and conflicts instead of filling them with confident prose.
4. For each action, define its source of authority and preconditions; for each completion claim, record a separate observation and criterion. Run `python3 checks/check_starter.py` for structural checks; they cannot validate meaning or authorisation.
5. Review with the project owner before treating any AI synthesis as a requirement or any derived document as accepted.

## Two routes

- **Standard / specification:** extract candidate project statements from permitted dialogue; check provenance, gaps and conflicts with the owner; prepare a specification retaining the goal; implement against accepted criteria.
- **Complex / Project Book:** keep a standalone author-intent statement without technical implementation details; establish an accepted Book as the project's conceptual reference, with an amendment procedure. Requirements, design, code and tests are derived and separately verified. Unimplemented intentions remain visible without being reported as delivered.

Choose by complexity, uncertainty and consequence of drift, not by document fashion. A technical specification may also describe goals; the Book route does not declare specifications useless.

## Structure and extension seams

- `templates/common/`: boundary, source register, current state, decision/evidence/action log.
- `templates/standard/`: reviewed extraction and conventional specification.
- `templates/complex/`: author intent, conceptual Book, amendment and traceability templates.
- `docs/PROCESS.md`: step-by-step intake and decision route.
- `docs/DECISIONS-AND-CHANGES.md`: ownership and correction protocol.
- `docs/EXTENSIONS.md`: optional research, doctrine, monitoring, and graph capabilities, **not installed here**.
- `examples/fictional-app/`: fictional contrast case; not evidence of real-world success.
- `farshmaster/`: two-pass intake of mixed raw text or attributed fragments, narrow candidate categories/scope and a non-canonical overview.
- `monitoring/`: optional basic read-only CLI for registered file presence and freshness of a declared observation; **not** an independent user-outcome sensor or a running service.
- `checks/`: offline structural smoke check only.

## Status and release boundary

This is an original starter **candidate**, not a copy or release of a private technology repository. No deployment, credential handling, automatic authority grants, live agent connection or continuous/external monitoring service is included. The included monitoring CLI is a bounded local structural check. It has not been tested on a real project. See `RELEASE-NOTES.md` for this preview's scope and `RELEASE-MANIFEST.json` for the exact file digests. Code, templates and accompanying documentation use the [MIT licence](LICENSE).
