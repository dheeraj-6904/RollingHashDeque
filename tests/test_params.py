"""Tests for :class:`hashdeque.HashParams`."""

from __future__ import annotations

import pytest

from hashdeque import DEFAULT_PARAMS, HashParams


def test_modular_inverses_are_correct():
    p = DEFAULT_PARAMS
    assert (p.base1 * p.inv1) % p.mod1 == 1
    assert (p.base2 * p.inv2) % p.mod2 == 1


def test_symbol_offset_avoids_zero():
    p = HashParams(offset=1)
    assert p.symbol("\x00") == 1  # null char must not map to 0
    assert p.char(p.symbol("Z")) == "Z"


def test_symbol_requires_single_character():
    p = DEFAULT_PARAMS
    with pytest.raises(ValueError):
        p.symbol("ab")
    with pytest.raises(ValueError):
        p.symbol("")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"base1": 1, "mod1": 1_000_000_007},   # base too small
        {"base1": 10, "mod1": 2},              # modulus too small
        {"offset": -1},                        # negative offset
    ],
)
def test_invalid_params_raise(kwargs):
    with pytest.raises(ValueError):
        HashParams(**kwargs)


def test_params_are_frozen():
    p = HashParams()
    with pytest.raises(Exception):
        p.base1 = 7  # type: ignore[misc]
