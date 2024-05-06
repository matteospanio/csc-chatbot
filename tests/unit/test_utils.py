import pytest
from hypothesis import given
from hypothesis import strategies as st

from chatbot import utils


def test_empty_depth_set():
    dic = {}
    utils.depth_set(dic, ["a", "b", "c"], 1)
    assert dic == {"a": {"b": {"c": 1}}}


@given(
    st.dictionaries(
        st.text("abc", min_size=1),
        st.dictionaries(
            st.text("abc", min_size=1),
            st.integers(),
        ),
    ),
)
def test_depth_set(input_dict):
    print(input_dict)
    utils.depth_set(input_dict, ["a", "b"], 1)
    assert input_dict["a"]["b"] == 1


def test_failing_depth_set():
    dic = {"a": 1}
    with pytest.raises(ValueError, match="keys must have at least one element"):
        utils.depth_set(dic, [], 0)


def test_flatten_dict():
    dic = {"a": {"b": {"c": 1}, "d": 5}}
    assert utils.flatten_dict(dic) == {"a.b.c": 1, "a.d": 5}

    dic = {}
    assert utils.flatten_dict(dic) == {}
