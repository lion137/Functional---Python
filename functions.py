# More functions on immutable list collection

from immutable_lists import *

def flatten(xs):
    if xs.is_empty():
        return Nil()
    elif is_list(xs.head):
        return concat(flatten(xs.head), flatten(xs.tail))
    else:
        return cons(xs.head, flatten(xs.tail))

def concat(xs, ys):
    """Concatenates two lists"""
    if xs.is_empty():
        return ys
    else:
        return cons(xs.head, concat(xs.tail, ys))

def append(xs, ys):
    @tail_recursive
    def append_help(lst1, lst2):
        if lst1.is_empty():
            return lst2
        else:
            recurse(lst1.tail, cons(lst1.head, lst2))
    return append_help(reverse(xs), ys)

def reverse(xs):
    @tail_recursive
    def rev_helper(lst1, lst2):
        if lst1.is_empty():
            return lst2
        else:
            return recurse(lst1.tail, cons(lst1.head, lst2))
    return rev_helper(xs, Nil())

def reverse_rec(xs):
    if xs.is_empty():
        return Nil()
    else:
        return concat(reverse_rec(xs.tail),  List(xs.head))

def is_list(xs):
    return isinstance(xs, Cons)


if __name__ == '__main__':
    lst0 = cons(1, cons(2, Nil()))
    lst1 = cons(lst0, cons(3, Nil()))
    lst3 = cons(lst1, lst0)
    lst_cons = List(1, 2)
    print(lst_cons)
    print(flatten(lst3))
    lst_test = List_from_iter(list(range(11)))
    lst_test2 = List_from_iter(list(range(15)))
    concat(lst_test, lst_test2)
    print(is_list(lst3))
    print(List(lst0))
    print("---------------reverse and append")
    lst_rev = List_from_iter(list(range(99999)))
    #print(reverse(lst_rev)) # -> OK
    append(lst_rev, List_from_iter(list(range(9999))))
    print(reverse_rec(lst0))
    print(concat(Nil(), Nil()))

