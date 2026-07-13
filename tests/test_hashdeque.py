"""Functional tests for the concrete :class:`HashDeque`."""

from __future__ import annotations

import pytest

import hashdeque
from hashdeque import DEFAULT_PARAMS, HashDeque, HashParams


def reference_hashes(text: str, params: HashParams = DEFAULT_PARAMS):
    """Independently compute the two polynomial hashes of ``text``."""
    h1 = h2 = 0
    for i, ch in enumerate(text):
        code = ord(ch) + params.offset
        h1 = (h1 + code * pow(params.base1, i, params.mod1)) % params.mod1
        h2 = (h2 + code * pow(params.base2, i, params.mod2)) % params.mod2
    return h1, h2


def current_hashes(d: HashDeque):
    return d._h1, d._h2


def test_package_metadata():
    assert hashdeque.__version__ == "0.0.3"
    assert set(hashdeque.__all__) >= {"HashDeque", "BaseHashDeque", "HashParams"}


def test_build_from_iterable_matches_reference():
    d = HashDeque("hello")
    assert len(d) == 5
    assert current_hashes(d) == reference_hashes("hello")


def test_push_back_matches_reference():
    d = HashDeque()
    for ch in "world":
        d.push_back(ch)
    assert list(d) == list("world")
    assert current_hashes(d) == reference_hashes("world")


def test_push_front_matches_reference():
    d = HashDeque()
    for ch in "abc":
        d.push_front(ch)  # yields "cba"
    assert "".join(d) == "cba"
    assert current_hashes(d) == reference_hashes("cba")


def test_pop_back_restores_hash():
    d = HashDeque("abcd")
    assert d.pop_back() == "d"
    assert list(d) == list("abc")
    assert current_hashes(d) == reference_hashes("abc")


def test_pop_front_restores_hash():
    d = HashDeque("abcd")
    assert d.pop_front() == "a"
    assert list(d) == list("bcd")
    assert current_hashes(d) == reference_hashes("bcd")


def test_mixed_operations_stay_consistent():
    d = HashDeque()
    d.push_back("b")
    d.push_front("a")   # ab
    d.push_back("c")    # abc
    d.push_front("z")   # zabc
    assert "".join(d) == "zabc"
    d.pop_front()       # abc
    d.pop_back()        # ab
    assert "".join(d) == "ab"
    assert current_hashes(d) == reference_hashes("ab")


def test_same_content_different_paths_are_equal():
    left = HashDeque("abc")
    right = HashDeque()
    right.push_front("c")
    right.push_front("b")
    right.push_front("a")
    assert left == right
    assert hash(left) == hash(right)


def test_different_content_not_equal():
    assert HashDeque("abc") != HashDeque("abd")
    assert HashDeque("abc") != HashDeque("ab")


def test_empty_deque():
    d = HashDeque()
    assert len(d) == 0
    assert not d
    assert list(d) == []
    assert HashDeque() == HashDeque()


def test_pop_from_empty_raises():
    d = HashDeque()
    with pytest.raises(IndexError):
        d.pop_back()
    with pytest.raises(IndexError):
        d.pop_front()


def test_unicode_symbols():
    text = "a\u00e9\U0001f600z"  # 'a', 'é', emoji, 'z'
    d = HashDeque(text)
    assert "".join(d) == text
    assert current_hashes(d) == reference_hashes(text)
    assert d == HashDeque(text)


def test_invalid_symbol_raises():
    d = HashDeque()
    with pytest.raises(ValueError):
        d.push_back("ab")  # not a single character
    with pytest.raises(ValueError):
        d.push_front("")


def test_verify_flag_confirms_contents():
    a = HashDeque("abc", verify=True)
    b = HashDeque("abc")
    assert a == b  # verification passes on genuine match


def test_clear_and_extend():
    d = HashDeque("abc")
    d.clear()
    assert len(d) == 0
    d.extend("xy")
    d.extendleft("12")  # front pushes -> "21xy"
    assert "".join(d) == "21xy"


def test_repr_roundtrip_content():
    d = HashDeque("hi")
    assert repr(d) == "HashDeque('hi')"


def test_custom_params_do_not_compare_equal_to_default():
    other = HashParams(base1=131, mod1=1_000_000_007, base2=137, mod2=1_000_000_009)
    a = HashDeque("abc")
    b = HashDeque("abc", params=other)
    assert a != b  # different params -> different fingerprints


def test_usage_example_from_readme():
    d = HashDeque()
    for ch in "hello":
        d.push_back(ch)
    first = d.hash()
    d.pop_front()
    assert d.hash() != first
    assert d == HashDeque("ello")
