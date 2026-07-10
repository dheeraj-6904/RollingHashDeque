# hashdeque

A string/bytes **deque** that maintains a **rolling hash** of its contents.
Powers of the base are precomputed, so the hash of the current sequence is
available in **O(1)** after each push/pop instead of rehashing everything.

- `push_front` / `push_back` — **O(1)**
- `pop_front` / `pop_back` — **O(1)**
- `hash()` of the current contents — **O(1)**
- equality between two `HashDeque` instances — **O(1)** (compares rolling hashes)

Useful for substring/window matching (Rabin–Karp style), deduplication over a
sliding window, and content-defined chunking.

> Note: the `HashDeque` implementation lands in a follow-up change; this is the
> packaging scaffold.

## Install

```bash
pip install hashdeque
```

Development setup:

```bash
uv venv
uv pip install -e ".[dev]"
```

## Usage

```python
from hashdeque import HashDeque

d = HashDeque()
for ch in b"hello":
    d.push_back(ch)
print(d.hash())     # rolling hash of "hello"
d.pop_front()       # drop 'h'
print(d.hash())     # rolling hash of "ello", O(1)

other = HashDeque(b"ello")
print(d == other)   # O(1) comparison
```

## Test

```bash
pytest
```

## Layout

```
hashdeque/
├── pyproject.toml
├── repo_structure.yaml         # enforced by the repo-structure pre-commit hook
├── .pre-commit-config.yaml
├── .github/workflows/publish.yml
├── src/hashdeque/
│   ├── __init__.py
│   └── py.typed
└── tests/
    └── test_hashdeque.py
```
