# hashdeque design

This document explains what `hashdeque` uses internally and how it works.

## Goal

`HashDeque` gives you:

- deque operations from both ends in **O(1)**
- rolling hash updates in **O(1)**
- equality check in **O(1)** in normal mode

It is useful when your sequence changes at the ends and you still need a cheap
fingerprint after each change.

## Core idea

For symbols `s[0..n-1]` (front to back), each rolling hash is:

`H = sum(s[i] * base^i) mod modulus`

The implementation stores **two independent hashes** (`h1`, `h2`) with
different `(base, modulus)` pairs to reduce collision risk.

## Data stored in HashDeque

- `_codes`: `collections.deque[int]` (symbols as integer code points + offset)
- `_h1`, `_h2`: current rolling-hash values
- `_pow1`, `_pow2`: `base^len` for each hash, used for O(1) push/pop updates
- `_params`: `HashParams` (bases, moduli, inverses, offset)
- `verify`: optional exact comparison mode for equality

## Why modular inverse is needed

When removing from the front (`pop_front`), the polynomial has to be shifted.
That means dividing by `base` modulo `modulus`, done by multiplying with
`base^-1` (modular inverse). Those inverses are precomputed in `HashParams`.

## O(1) update formulas

For current length `n`:

- `push_back(c)`: `H = H + c * base^n`
- `pop_back()`: `H = H - c * base^(n-1)`
- `push_front(c)`: `H = c + base * H`
- `pop_front()`: `H = (H - c) * base^-1`

All operations are modulo the corresponding prime modulus.

## Equality model

The `fingerprint` includes:

- length
- both hash values
- hash parameters (bases and moduli)

So `a == b` can be checked in O(1) by comparing fingerprints.

If `verify=True` is enabled for either deque, equality also checks exact
contents after fingerprint match.

## Files and responsibilities

- `src/hashdeque/base.py`: abstract contract + shared behavior (`==`, aliases)
- `src/hashdeque/params.py`: hash configuration and derived inverses
- `src/hashdeque/deque.py`: concrete rolling-hash deque implementation
- `tests/`: functional and contract tests
