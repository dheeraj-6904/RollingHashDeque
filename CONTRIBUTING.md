# Contributing to hashdeque

Thanks for contributing.

## Setup

```bash
uv venv
uv pip install -e ".[dev]"
```

## Run tests

```bash
uv run pytest
```

## Make changes

1. Create a branch from `main`.
2. Keep changes focused and small.
3. Update tests/docs when behavior changes.
4. Ensure tests pass locally.

## Raise a pull request

1. Push your branch to GitHub.
2. Open a PR to `main`.
3. In PR description, include:
   - what changed
   - why it changed
   - any behavior impact
4. Link related issue(s), if any.

## Code style notes

- Follow existing module structure and naming patterns.
- Keep public API changes intentional and documented.
- Prefer clear, small functions over clever shortcuts.
