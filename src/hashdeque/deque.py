"""Concrete polynomial double rolling-hash deque.

``HashDeque`` maintains two independent polynomial hashes of its contents. For a
sequence ``s[0..n-1]`` (index 0 = front) each hash is::

    H = sum(s[i] * base**i)  (mod modulus)

Precomputed powers and a modular inverse of the base let every end operation run
in O(1):

* ``push_back(c)``  -> ``H += c * base**n``          then ``n += 1``
* ``pop_back()``    -> ``H -= s[n-1] * base**(n-1)``  then ``n -= 1``
* ``push_front(c)`` -> ``H  = c + base * H``          then ``n += 1``
* ``pop_front()``   -> ``H  = (H - s[0]) * base**-1`` then ``n -= 1``

The current contents (with length) are exposed as an O(1) ``fingerprint``, so two
deques compare in O(1). Using two moduli makes an accidental collision
astronomically unlikely; pass ``verify=True`` to additionally confirm contents.
"""

from __future__ import annotations

from collections import deque
from typing import Hashable, Iterable, Iterator

from .base import BaseHashDeque
from .params import DEFAULT_PARAMS, HashParams


class HashDeque(BaseHashDeque):
    """A deque of characters with an O(1) rolling hash and O(1) equality."""

    def __init__(
        self,
        initial: Iterable[str] = "",
        *,
        params: HashParams = DEFAULT_PARAMS,
        verify: bool = False,
    ) -> None:
        self._params = params
        self.verify = verify
        self._codes: "deque[int]" = deque()
        self._h1 = 0
        self._h2 = 0
        self._pow1 = 1  # params.base1 ** len(self)  (mod params.mod1)
        self._pow2 = 1  # params.base2 ** len(self)  (mod params.mod2)
        self.extend(initial)

    @property
    def params(self) -> HashParams:
        """The hash parameters this deque was constructed with."""
        return self._params

    def push_back(self, char: str) -> None:
        p = self._params
        code = p.symbol(char)
        self._h1 = (self._h1 + code * self._pow1) % p.mod1
        self._h2 = (self._h2 + code * self._pow2) % p.mod2
        self._pow1 = (self._pow1 * p.base1) % p.mod1
        self._pow2 = (self._pow2 * p.base2) % p.mod2
        self._codes.append(code)

    def push_front(self, char: str) -> None:
        p = self._params
        code = p.symbol(char)
        self._h1 = (code + p.base1 * self._h1) % p.mod1
        self._h2 = (code + p.base2 * self._h2) % p.mod2
        self._pow1 = (self._pow1 * p.base1) % p.mod1
        self._pow2 = (self._pow2 * p.base2) % p.mod2
        self._codes.appendleft(code)

    def pop_back(self) -> str:
        if not self._codes:
            raise IndexError("pop_back from an empty HashDeque")
        p = self._params
        code = self._codes.pop()
        self._pow1 = (self._pow1 * p.inv1) % p.mod1  # now base1 ** (n-1)
        self._pow2 = (self._pow2 * p.inv2) % p.mod2
        self._h1 = (self._h1 - code * self._pow1) % p.mod1
        self._h2 = (self._h2 - code * self._pow2) % p.mod2
        return p.char(code)

    def pop_front(self) -> str:
        if not self._codes:
            raise IndexError("pop_front from an empty HashDeque")
        p = self._params
        code = self._codes.popleft()
        self._h1 = ((self._h1 - code) * p.inv1) % p.mod1
        self._h2 = ((self._h2 - code) * p.inv2) % p.mod2
        self._pow1 = (self._pow1 * p.inv1) % p.mod1
        self._pow2 = (self._pow2 * p.inv2) % p.mod2
        return p.char(code)

    def __len__(self) -> int:
        return len(self._codes)

    def __iter__(self) -> Iterator[str]:
        char = self._params.char
        return (char(code) for code in self._codes)

    def __str__(self) -> str:
        return "".join(self)

    @property
    def fingerprint(self) -> Hashable:
        p = self._params
        return (
            len(self._codes),
            self._h1,
            self._h2,
            p.base1,
            p.mod1,
            p.base2,
            p.mod2,
        )
