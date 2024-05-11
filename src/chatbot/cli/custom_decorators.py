"""Decorators for the CLI commands."""

import inspect
import re


def __parse_metadata(text: str) -> str | None:
    pattern = r"'(.*?)'"

    matches = re.search(pattern, text)

    if matches is None:
        return None

    return matches.group(1)


def docstring_decorator(help_text):
    """Add a formatted help text to the docstring of the function."""

    def wrapper(func):
        argument_doc = help_text + "\n\n\b\n"
        args = inspect.signature(func).parameters

        for param in args.values():
            if "Annotated" in str(param.annotation):
                help_str = __parse_metadata(str(param.annotation))
                argument_doc += f"{param.name.upper()}\t{help_str}\n"

        func.__doc__ = argument_doc

        return func

    return wrapper
