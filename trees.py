# define an abstract data - binary tree - pairs and functional abstraction

from functional_tools_python.immutable_lists import *

def construct_tree(val, left, right):
    """constructs a tree as a List, holds
    as a first elem a value in a node, second and
    third elements are left, right branches (also trees)"""
    return List(val, left, right)

def value(tree):
    """returns a value holds in a tree node"""
    return tree[0]


def left(tree):
    """returns a left branch of the tree"""
    return tree[1]

def right(tree):
    """returns a right branch of the tree"""
    return tree[2]

def contains_tree(a, tree):
    """check if tree contains an
    elemnt a"""
    if tree.is_empty():
        return False
    elif a == value(tree):
        return True
    elif a < value(tree):
        return contains_tree(a, left(tree))
    elif a > value(tree):
        return contains_tree(a, right(tree))


if __name__ == '__main__':
    tr1 = construct_tree(3, construct_tree(2, construct_tree(1, Nil(), Nil()), Nil()), construct_tree(4, Nil(), Nil()))
    print(contains_tree(0, tr1)) # -> False
    print(contains_tree(1, tr1)) # -> True
    print(contains_tree(4, tr1)) # -> True

