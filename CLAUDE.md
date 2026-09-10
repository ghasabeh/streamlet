# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What Streamlet is

A fluent, **lazy** stream-processing library for Python, modeled after Java's Streams API:

```python
Stream.of(...).filter(...).map(...).take(10).to_list()
```

The goal is to make `itertools`' power reachable through clean, chainable syntax. It is a
**portfolio project** — each feature was chosen to demonstrate a specific Python capability, so
prefer the idiomatic-and-showcase-worthy implementation over the shortest one:

| Capability | Where it shows up |
|---|---|
| Generators / laziness | Intermediate ops (`map`, `filter`, `take`, `skip`, `flat_map`, `distinct`) build a pipeline; **nothing executes until a terminal op runs** |
| Magic methods | `__iter__`, `__repr__`, and `__or__` for pipe-style chaining |
| Context managers | `Stream.from_file(path)` via `__enter__`/`__exit__`; the handle must close on early `break` or exception |
| Async | `AsyncStream[T]` with `__aiter__`, concurrent map over `asyncio.TaskGroup` with bounded concurrency |
| Generics | `Stream[T]` via `typing.Generic`, for real IDE autocomplete |
| Terminal ops | `to_list`, `reduce`, `sum`, `count`, `first`, `any`, `all`, `group_by` |

Target is a published PyPI package (the name is confirmed available).

## Project state

Early scaffolding — `src/streamlet/__init__.py` holds only a `main()` stub wired to the `streamlet`
console script. **None of the library above exists yet.** M1 (tooling) is in progress; everything
from `Stream` onward is still backlog, so expect to create modules rather than find them.

Roadmap milestones, tracked in Linear: **M1** scaffolding/lint/CI · **M2** core `Stream[T]`,
intermediate + terminal ops, laziness tests · **M3** `__or__`, constructors, `group_by`, edge cases
· **M4** `from_file` resource streams · **M5** `AsyncStream` · **M6** docstrings, `mypy --strict`,
README, PyPI release.

## Linear

Issues live in the **Thread-Safe** workspace (team key `THR`), project *Streamlet*
(`d0777fc2-700b-46ee-abc4-88524793410f`).

The Linear **MCP connector is authenticated to a different workspace (Narmin) and cannot see `THR`
issues** — its tools return "team not found". Query the GraphQL API directly instead, using the key
in `.env`:

```bash
set -a && . ./.env && set +a && curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"query { issue(id: \"THR-6\") { title state{name} branchName } }"}'
```

## Commands

Dependencies are managed with **uv** (`uv_build` is the build backend, `uv.lock` is committed).
Dev tools live in `[dependency-groups] dev`, which uv installs by default — no extra flags needed.

```bash
uv sync                    # install project + dev tools into .venv
uv run ruff check .        # lint
uv run ruff format .       # format (add --check to report without rewriting)
uv run mypy                # type check (paths come from [tool.mypy] files)
uv run pytest              # tests
uv run pytest tests/test_smoke.py::test_main_run   # single test
uv run streamlet           # run the console entry point
```

Run all four gates the way CI does before pushing:

```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
```

`pre-commit` runs ruff (with `--fix`) and mypy on every `git commit`. If a hook rewrites a file the
commit aborts by design — `git add -A` and commit again. Install it once per clone with
`uv run pre-commit install`. Hook versions in `.pre-commit-config.yaml` are pinned separately from
`pyproject.toml`, so bump both together (`uv run pre-commit autoupdate`).

CI (`.github/workflows/ci.yml`) runs the same four steps across Python 3.10–3.14 via `uv sync`, so
it honors `uv.lock` rather than resolving fresh. It triggers on every PR and on pushes to `main`
and `dev`.

## Python version

`requires-python` is `>=3.10` and CI tests 3.10 through 3.14, while `.python-version` pins local
dev to 3.14. **Code must stay valid on 3.10** — don't reach for newer syntax because the local
interpreter accepts it. Both `ruff` (`target-version = "py310"`) and `mypy`
(`python_version = "3.10"`) are configured to enforce that floor locally, so violations surface
before CI.

## Conventions

- Branches: `aghasabeh/thr-<n>-<milestone>-<kebab-slug>` (e.g. `aghasabeh/thr-6-m1-linttype-check-config-ruff-mypy-pre-commit`).
- Commits and PR titles: `THR-<n>: M<milestone>: <description>`.
- **Branching model:** feature branches PR into `dev`; `main` is release-only. Always open PRs with
  `gh pr create --base dev` — `main` is the GitHub default branch, so the base must be set
  explicitly or the PR targets the wrong place.
- `.env` is gitignored and holds `LINEAR_API_KEY`.
