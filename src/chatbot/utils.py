"""Utility functions that are used in the chatbot."""

from collections.abc import MutableMapping
from typing import Any


def flatten_dict(d, parent_key="", sep="."):
    """Flatten a dictionary."""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def depth_set(d: dict, keys: list[str], value: Any) -> None:
    """Set a value in a nested dictionary."""
    if len(keys) == 0:
        msg = "keys must have at least one element"
        raise ValueError(msg)

    if len(keys) == 1:
        d[keys[0]] = value
        return

    if keys[0] not in d:
        d[keys[0]] = {}

    depth_set(d[keys[0]], keys[1:], value)
