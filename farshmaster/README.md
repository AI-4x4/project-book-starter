# Farshmaster: bounded first slice

**Language / Язык:** [English](README.md) · [Русский](README.ru.md) · [Home / Главная](../README.md)

**Two passes:** (1) process permitted JSONL fragments with supplied categories or suggest narrow heuristic labels for recognisable phrases; ambiguous content remains `unknown`. (2) assemble a reviewable proto-idea *candidate* as references to the original fragments, retaining declared conflicts, assumptions and gaps. Nothing is written to the Project Book and no owner decision is made by the tool.

The 12 category names come from an early illustrative discussion, not an approved final taxonomy: `intention`, `desired_result`, `problem`, `example`, `fact`, `assumption`, `preference`, `constraint`, `decision`, `question`, `contradiction`, `unknown`. A `decision` label denotes a fragment type, not proof of authority or approval. A proposed third layer for the desired-outcome model is not implemented.

For unlabelled mixed text, run from the repository root:

```sh
python3 -m farshmaster.core --raw --source-id synthetic --source-role author --project-term "Проект Соседи" examples/fictional-app/mixed-raw.txt
```

A project-term match is only a *candidate* relation to the project. Nonmatches remain in `needs_scope_review`, not in an "irrelevant" discard pile. The tool preserves nonblank lines with source, line position and hash; it does not split several ideas within one line. Output includes the original text on stdout: keep real private inputs and outputs in an appropriately protected location, never in the public repository.

JSONL input uses one object per line, for example `{"id":"A","source":"source ID/time","text":"...","category":"intention","scope":"project","contradicts":["B"]}`. `id`, `source`, `text` are required; `category`, `scope`, `contradicts` are optional. Without `scope`, a fragment stays outside the proposed project proto-idea until reviewed. Run `python3 -m farshmaster.core /path/to/permitted-fragments.jsonl`; this prints to stdout only. Basic tests: `python3 -m unittest discover -s farshmaster -p 'test_*.py'`.

**Limit:** this is deterministic, narrow routing and assembly, not an agent that understands arbitrary messy text. Semantic classification, completeness of provenance, quality of synthesis, the owner's confirmation of intent and real-world outcomes are not verified.
