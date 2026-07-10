"""Tests for the abstract :class:`hashdeque.BaseHashDeque` contract."""

from __future__ import annotations

import pytest

from hashdeque import BaseHashDeque, HashDeque


def test_base_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseHashDeque()  # type: ignore[abstract]


def test_deque_is_a_base_hash_deque():
    assert isinstance(HashDeque(), BaseHashDeque)


def test_aliases_match_primitive_operations():
    d = HashDeque()
    d.append("b")       # push_back
    d.appendleft("a")   # push_front
    assert "".join(d) == "ab"
    assert d.popleft() == "a"


def test_eq_with_non_deque_is_false():
    d = HashDeque("abc")
    assert d != "abc"
    assert (d == 42) is False


def test_hashable_in_set():
    seen = {HashDeque("abc"), HashDeque("abc"), HashDeque("abd")}
    assert len(seen) == 2
