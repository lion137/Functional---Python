# Recursive definition of  binary search tree (immutable)
# I follows a grammar:
# Binary-search-tree :: = () | (Val Binary-search-tree Binary-search-tree) Val should support >, <, =
# is empty or it's a list of Int and two binary trees
# there's gonna be right and left subtree
# The interface strictly follow this definition

from _collections_abc import ABCMeta, abstractmethod

class Nil_tree:
    """class Nil_tree, the empty tree"""

    def is_empty(self):
        return True

    def left(self):
        return Exception("Empty")

    def right(self):
        return Exception("Empty")

    def __str__(self):
        return "()"


class Binary_tree:
    """Class Binary_tree, the non empty tree: ( val, left, right)"""

    def __init__(self, _item, _left, _right):
        self.item = _item
        self.left = _left
        self.right = _right

    def is_empty(self):
        return False


class Tree(metaclass=ABCMeta):
    @abstractmethod
    def is_empty(self):
        pass

    def item(self):
        pass

    def left(self):
        pass

    def right(self):
        pass


Tree.register(Nil_tree);
Tree.register(Binary_tree)