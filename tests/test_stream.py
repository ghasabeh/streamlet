from itertools import count

import pytest

from streamlet import Stream, StreamConsumedError


def test_wraps_an_iterable() -> None:
    assert list(Stream([1, 2, 3])) == [1, 2, 3]


def test_empty_stream() -> None:
    assert list(Stream([])) == []


def test_accepts_a_generator() -> None:
    assert list(Stream(n * 2 for n in range(3))) == [0, 2, 4]


def test_does_not_consume_infinite_source_on_construction() -> None:
    stream = Stream(count())
    assert next(iter(stream)) == 0


def test_second_iteration_raises() -> None:
    stream = Stream([1, 2, 3])
    list(stream)
    with pytest.raises(StreamConsumedError):
        list(stream)


def test_repr_reflects_state() -> None:
    stream = Stream([1, 2, 3])
    assert repr(stream) == "<Stream lazy>"
    list(stream)
    assert repr(stream) == "<Stream consumed>"
