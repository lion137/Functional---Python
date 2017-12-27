# Cons lists, tail recursion decorator, functions on lists:

from _collections_abc import ABCMeta, abstractmethod


# Recurse Class and tail recursion decorator:


class Recurse(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def recurse(*args, **kwargs):
    raise Recurse(*args, **kwargs)


def tail_recursive(f):
    def decorated(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except Recurse as r:
                args = r.args
                kwargs = r.kwargs
                continue

    return decorated


# immutable Cons list and methods:
from _collections_abc import ABCMeta, abstractmethod

class Nil:

    def is_empty(self):
        return True

    def head(self):
        return Exception("Exception: Empty list")

    def tail(self):
        return Exception("Exception: Empty list")

    def __str__(self):
        return "()"


class Cons:

    def __init__(self, _head, _list_tail=Nil()):
        self.head = _head
        self.tail = _list_tail

    def is_empty(self):
        return False

    def __getitem__(self, index):
        return nth(index, self)

    def __str__(self):
        cur = self
        out = ''
        while (isinstance(cur, Cons) or isinstance(cur, Nil)) and (not cur.is_empty()):
            out += ' ' + str(cur.head)
            cur = cur.tail

        out = '(' + out + ')'
        return out


class ImmutableList(metaclass=ABCMeta):
    @abstractmethod
    def is_empty(self):
        pass

    def head(self):
        pass

    def tail(self):
        pass


ImmutableList.register(Nil);
ImmutableList.register(Cons)


def cons(elem, xs):
    """Cons element elem to the list"""
    return Cons(elem, xs)


def List(*args_list):
        """Crates immutable list from arguments"""
        tmp_list = Cons(args_list[len(args_list) - 1], Nil())
        for x in range(len(args_list) - 2, -1, -1):
            tmp_list = Cons(args_list[x], tmp_list)
        return tmp_list


def List_from_iter(args_list):
    """Crates a list form list"""
    tmp_list = Cons(args_list[len(args_list) - 1], Nil())
    for x in range(len(args_list) - 2, -1, -1):
        tmp_list = Cons(args_list[x], tmp_list)
    return tmp_list





@tail_recursive
def length(xs, cnt=0):
    """Returns length of a list O(n)"""
    if isinstance(xs, Nil):
        return cnt
    else:
        return recurse(xs.tail, cnt + 1)


@tail_recursive
def nth(n, xs):
    """Returns nt-h (0 based indexing) elemt of the list,
    throws an exception when out of range"""
    if isinstance(xs, Nil):
        return Exception("Out Of Bound")
    if n == 0:
        return xs.head
    else:
        return recurse(n - 1, xs.tail)


def sum_list(xs):
    if xs.is_empty():
        return 0
    else:
        return xs.head + sum_list(xs.tail)


def sum_list_iter(xs):
    @tail_recursive
    def iter_helper(ys, acc):
        if ys.is_empty():
            return acc
        else:
            return recurse(ys.tail, acc + ys.head)
    return iter_helper(xs, 0)

if __name__ == '__main__':
    '''x = cons(1, cons(2, Nil()))
    print_list(x)
    List1 = list(range(10000))
    imm_list = List(List1)
    print_list(imm_list)
    print(nth(9999, imm_list))
    print(length(imm_list))
    print(imm_list[10])
    y = Cons(1, Nil())
    print(y.tail)'''
    lst = List_from_iter(list(range(1, 4)))
    print(lst) # -> 6
    lst2 = List_from_iter(list(range(1, 10000)))
    #print(sum_list(lst2))  # Bang! Stos zjedzony!
    print(sum_list_iter(lst2) == sum(list(range(1, 10000)))) # -> True
    print(sum(list(range(1, 10000))))
    lst3 = cons(1, cons(2, Nil()))
    lst4 = cons(lst3, cons(3, Nil()))
    print("to str", lst4)
    print()
