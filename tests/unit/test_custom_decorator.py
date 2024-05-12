from typing import Annotated

from chatbot.cli.custom_decorators import docstring_decorator


def test_decorator_without_annotation():
    @docstring_decorator("This is a test")
    def test_func():
        pass

    assert test_func.__doc__ == "This is a test\n\n\b\n"


def test_decorator_with_annotation():
    @docstring_decorator("This is a test")
    def test_func(arg: Annotated[str, "str"]):
        pass

    assert "This is a test\n\n\b\nARG\tstr\n" in test_func.__doc__
