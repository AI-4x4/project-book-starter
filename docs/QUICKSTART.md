# Preview quickstart

Requires Python 3.10+; no packages or network requests. Run all commands from the repository root. On Windows, use `python` if that is the name of your Python executable. [Русская версия](QUICKSTART.ru.md).

## 1. Mixed input

```sh
python3 -m farshmaster.core --raw --source-id synthetic --source-role author --project-term "Проект Соседи" examples/fictional-app/mixed-raw.txt
```

All four original lines remain in `categories`, with order, source and SHA-256. The first line gets an `intention` candidate and a `KEYWORD_CANDIDATE` project-scope mark. The other three remain in `needs_scope_review`; absence of the project's name is not proof of irrelevance. `owner_validation` stays `PENDING`, and `discarded_fragment_ids` stays empty. This is a traceable index, not an automatically understood intent.

## 2. Human review

Compare each line with its source. In the fictional example, the constraint about neighbours without smartphones concerns the project, although the code misses that connection. Ask the owner about the company and colour lines. The example `intake.jsonl` illustrates manual labels and leaves unreviewed fragments uncertain.

```sh
python3 -m farshmaster.core examples/fictional-app/intake.jsonl
```

The 12 category names are illustrative. A `decision` label does not attest the author's authority; owner review and acceptance of intent are human steps.

## 3. Project Book or specification

Create a separate project directory outside the starter. Copy the contents of `templates/common/` and either `templates/complex/` or `templates/standard/`. Record the notice-delivery goal, sources, accepted decision and observable criterion in the new documents. Separate accepted decisions from proposals. The fictional scenario is explained in `examples/fictional-app/README.md`; no real neighbours or deliveries were tested.

```sh
python3 -m monitoring.basic_monitor /path/to/project
```

`OK` attests only that a nonempty document exists. The outcome remains `NOT_TESTED` without independent verification. Even a fresh declaration of success does not become a verified result.

## 4. Basic checks

```sh
python3 checks/check_starter.py
python3 -m unittest discover -s farshmaster -p 'test_*.py'
python3 -m unittest discover -s monitoring -p 'test_*.py'
```

These cover structure and 9 + 7 basic local tests, not real-project utility. Storing private raw data in this public repository is not part of the procedure.
