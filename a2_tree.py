"""
Tree class and functions.
"""
from typing import Any


class TreeNode:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    """

    def __init__(self, value=None, children=None, score=None) -> None:
        """
        Create Tree self with content value and 0 or more children
        """
        self.value = value
        self.children = children[:] if children is not None else []
        self.score = score


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
