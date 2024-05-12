"""Utility functions that are used in the chatbot."""

from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any


def flatten_dict(
    d: Mapping[str, Any],
    parent_key: str = "",
    sep: str = ".",
) -> dict[str, Any]:
    """Flatten a dictionary."""
    items: list[Any] = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, Mapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def depth_set(d: MutableMapping[str, Any], keys: Sequence[str], value: Any) -> None:
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
