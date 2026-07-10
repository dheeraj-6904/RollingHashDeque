# hashdeque

A **deque of characters** (any Unicode symbol) that maintains a **rolling hash**
of its contents. Powers of the base are precomputed, so the hash of the current
sequence is available in **O(1)** after each push/pop instead of rehashing
everything.

- `push_front` / `push_back` — **O(1)**
- `pop_front` / `pop_back` — **O(1)**
- `hash()` of the current contents — **O(1)**
- equality between two `HashDeque` instances — **O(1)** (compares rolling hashes)

Useful for substring/window matching (Rabin–Karp style), deduplication over a
sliding window, and content-defined chunking.

## Install

```bash
pip install hashdeque
```

## Quick usage

```python
from hashdeque import HashDeque

d = HashDeque()
for ch in "hello":
    d.push_back(ch)
print(d.hash())     # rolling-hash fingerprint of "hello"
d.pop_front()       # drop 'h'
print(d.hash())     # fingerprint of "ello", computed in O(1)

other = HashDeque("ello")
print(d == other)   # True, O(1) comparison

d.verify = True     # opt in to exact verification on a hash match
```

## API at a glance

- `HashDeque(initial="", *, params=DEFAULT_PARAMS, verify=False)`
- `push_front(char)`, `push_back(char)`
- `pop_front()`, `pop_back()`
- `hash()` / `fingerprint`
- `extend(chars)`, `extendleft(chars)`, `clear()`

## Docs for contributors and internals

- [Design and internals](docs/design.md)
- [Contributing guide](CONTRIBUTING.md)
