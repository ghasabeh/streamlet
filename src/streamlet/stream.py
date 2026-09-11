from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


class StreamConsumedError(RuntimeError):
    """Raised when a stream is iterated more than once."""


class Stream(Generic[T]):
    """A lazy, single-use stream over an iterable.

    Wraps an iterator and defers all work until iteration begins.
    """

    __slots__ = ("_consumed", "_iterator")

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterator: Iterator[T] = iter(iterable)
        self._consumed = False

    def __iter__(self) -> Iterator[T]:
        if self._consumed:
            raise StreamConsumedError("this stream has already been consumed")
        self._consumed = True
        return self._iterator

    def __repr__(self) -> str:
        state: str = "consumed" if self._consumed else "lazy"
        return f"<Stream {state}>"
