"""Streamlet — a fluent, lazy stream-processing library for Python."""

from streamlet.stream import Stream, StreamConsumedError

__all__ = ["Stream", "StreamConsumedError"]


def main() -> None:
    print("Hello from streamlet!")
