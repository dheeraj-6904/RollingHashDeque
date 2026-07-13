"""Abstract base class for hash-maintaining double-ended queues.

``BaseHashDeque`` defines the public contract (the four O(1) end mutations plus
an O(1) ``fingerprint``) and implements every behaviour that can be expressed in
terms of that contract: equality, hashing, iteration helpers and deque-style
aliases. Concrete hashing strategies subclass this without changing it, which
keeps the hierarchy open for extension but closed for modification.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Hashable, Iterable, Iterator


class BaseHashDeque(ABC):
    """A double-ended queue of single-character symbols with an O(1) fingerprint."""

    #: Whether ``==`` should verify contents when fingerprints already match.
    verify: bool = False

    # --- Abstract primitives that concrete subclasses must provide ---------

    @abstractmethod
    def push_front(self, char: str) -> None:
        """Prepend ``char`` in O(1)."""

    @abstractmethod
    def push_back(self, char: str) -> None:
        """Append ``char`` in O(1)."""

    @abstractmethod
    def pop_front(self) -> str:
        """Remove and return the leftmost character in O(1)."""

    @abstractmethod
    def pop_back(self) -> str:
        """Remove and return the rightmost character in O(1)."""

    @abstractmethod
    def __len__(self) -> int:
        """Number of symbols currently stored."""

    @abstractmethod
    def __iter__(self) -> Iterator[str]:
        """Iterate over the symbols from front to back."""

    @property
    @abstractmethod
    def fingerprint(self) -> Hashable:
        """An O(1) hashable key identifying the current contents and length."""

    # --- Behaviour derived from the primitives ----------------------------

    def hash(self) -> Hashable:
        """Return the current O(1) rolling-hash fingerprint."""
        return self.fingerprint

    # deque-style aliases so the type feels familiar
    def appendleft(self, char: str) -> None:
        self.push_front(char)

    def append(self, char: str) -> None:
        self.push_back(char)

    def pop(self) -> str:
        return self.pop_back()

    def popleft(self) -> str:
        return self.pop_front()

    def popright(self) -> str:
        return self.pop_back()

    def extend(self, chars: Iterable[str]) -> None:
        """Append each character of ``chars`` to the back."""
        for char in chars:
            self.push_back(char)

    def extendleft(self, chars: Iterable[str]) -> None:
        """Prepend each character of ``chars`` to the front (order reversed)."""
        for char in chars:
            self.push_front(char)

    def clear(self) -> None:
        """Remove all symbols."""
        while len(self):
            self.pop_back()

    def __bool__(self) -> bool:
        return len(self) > 0

    def _should_verify(self, other: "BaseHashDeque") -> bool:
        return bool(self.verify or other.verify)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseHashDeque):
            return NotImplemented
        if self.fingerprint != other.fingerprint:
            return False
        if self._should_verify(other):
            return list(self) == list(other)
        return True

    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __hash__(self) -> int:
        return hash(self.fingerprint)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({''.join(self)!r})"
