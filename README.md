# RollingHashDeque

A double-ended queue (deque) that maintains a **rolling hash** of its contents,
so the hash of the current window is available in O(1) after each push/pop
instead of rehashing the whole sequence.

Useful for substring/window matching (Rabin–Karp style), deduplication over a
sliding window, and content-defined chunking.

## Install (dev)

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -e ".[dev]"
```

## Usage

```python
from rolling_hash_deque import RollingHashDeque

d = RollingHashDeque()
for ch in b"hello":
    d.push_back(ch)
print(d.hash())     # rolling hash of "hello"
d.pop_front()       # drop 'h'
print(d.hash())     # rolling hash of "ello", O(1)
```

## Test

```bash
pytest
```

## Layout

```
RollingHashDeque/
├── pyproject.toml
├── src/rolling_hash_deque/
│   └── __init__.py
└── tests/
    └── test_rolling_hash_deque.py
```
