"""Hash parameters for polynomial rolling hashes.

``HashParams`` is the extension point of the library: it bundles the bases,
moduli and derived modular inverses used by a concrete hash deque. New hashing
configurations can be introduced by creating additional ``HashParams`` instances
(or subclasses) without modifying any existing deque class.

Two deques can only be compared meaningfully when they share identical
parameters; the active parameters are therefore folded into every fingerprint.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _modinv(value: int, modulus: int) -> int:
    """Return the modular inverse of ``value`` mod a **prime** ``modulus``."""
    return pow(value % modulus, modulus - 2, modulus)


@dataclass(frozen=True)
class HashParams:
    """Immutable configuration for a polynomial double rolling hash.

    Attributes:
        base1, base2: Polynomial bases for the two independent hashes.
        mod1, mod2: Prime moduli for the two independent hashes.
        offset: Added to every code point so no symbol maps to ``0`` (which
            would make a leading symbol invisible to the hash).
    """

    base1: int = 1_500_007
    mod1: int = 1_000_000_007
    base2: int = 1_500_019
    mod2: int = 1_000_000_009
    offset: int = 1

    inv1: int = field(init=False, repr=False, compare=False)
    inv2: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for base, mod in ((self.base1, self.mod1), (self.base2, self.mod2)):
            if mod < 3:
                raise ValueError("moduli must be primes greater than 2")
            if not 2 <= base < mod:
                raise ValueError("each base must satisfy 2 <= base < modulus")
        if self.offset < 0:
            raise ValueError("offset must be non-negative")
        object.__setattr__(self, "inv1", _modinv(self.base1, self.mod1))
        object.__setattr__(self, "inv2", _modinv(self.base2, self.mod2))

    def symbol(self, char: str) -> int:
        """Map a single-character string to its offset code point."""
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("symbols must be single-character strings")
        return ord(char) + self.offset

    def char(self, code: int) -> str:
        """Inverse of :meth:`symbol`: turn an offset code point back to a char."""
        return chr(code - self.offset)


DEFAULT_PARAMS = HashParams()
"""Shared default parameters. Deques must use equal params to compare equal."""
