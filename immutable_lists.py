# Cons lists, tail recursion decorator, functions on lists:

from _collections_abc import ABCMeta, abstractmethod

from operator import *


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
        i = 0
        while (isinstance(cur, Cons) or isinstance(cur, Nil)) and (not cur.is_empty()) and i < 20:
            out += ' ' + str(cur.head)
            cur = cur.tail
            i += 1

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


def cons(elem, xs=Nil()):
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


def flatten(xs):
    if xs.is_empty():
        return Nil()
    elif is_list(xs.head):
        return concat(flatten(xs.head), flatten(xs.tail))
    else:
        return cons(xs.head, flatten(xs.tail))


def concat(xs, ys):
    @tail_recursive
    def concat_help(lst1, lst2):
        if lst1.is_empty():
            return lst2
        else:
            recurse(lst1.tail, cons(lst1.head, lst2))
    return concat_help(reverse(xs), ys)

def reverse(xs):
    @tail_recursive
    def rev_helper(lst1, lst2):
        if lst1.is_empty():
            return lst2
        else:
            return recurse(lst1.tail, cons(lst1.head, lst2))
    return rev_helper(xs, Nil())


def is_list(xs):
    return isinstance(xs, Cons) or isinstance(xs, Nil)


# HOF's

def cons_map(f, xs):
    """returns cons list with function f
    mapped over cons list xs"""
    @tail_recursive
    def helper(f, xs, ys):
        if xs.is_empty():
            return ys
        else:
            return recurse(f, xs.tail, Cons(f(xs.head), ys))
    return helper(f, reverse(xs), Nil())


def cons_filter(p, xs):
    """takes predicate p and cons list xs
    returns list filtered by predicate"""
    @tail_recursive
    def helper(pr, xs, ys):
        if xs.is_empty():
            return ys
        elif pr(xs.head):
            return recurse(pr, xs.tail, cons(xs.head, ys))
        else:
            return recurse(pr, xs.tail, ys)
    return helper(p, reverse(xs), Nil())

def cons_reduce(f, xs, start):
    """fold left, takes a function f, sequence xs and
    strating point start and returns function applied
    to the starting point and the first element of the collection
    outcome of this two the second element, etc... Ex.:
    cons_reduce(add, [1, 2, 3], 0) = 6"""
    @tail_recursive
    def helper(fn, ys ,acc):
        if ys.is_empty():
            return acc
        else:
            return recurse(fn, ys.tail, fn(acc, ys.head))
    return helper(f, xs, start)


# stream functions:


def make_stream(fn, arg):
    """Takes function fn ,argument and returns stream"""
    f = lambda x: cons(x, lambda : f(fn(x, arg)))
    return lambda: f(arg)


def stream_while(s, n):
    """Takes stream s and number n and returns a list
    of n values of stream in order"""
    if n == 0:
        return Nil()
    else:
        return cons(s().head, stream_while(s().tail, n - 1))


def stream_reader(p, s):
    """read a stream s until predicate p holds"""
    current = s()
    tmp_list = Nil()
    while p(current.head):
        tmp_list = cons(current.head, tmp_list)
        current = current.tail()
    return reverse(tmp_list)

def stream_map(f, s):
    """takes stream s and function f and return
    stream with f mapped over input stream s"""
    return lambda: cons(f(s().head), stream_map(f, s().tail))


def stream_filter(p, s):
    """Takes a predicate p and a stream s and
    returns the stream filtered by the predicate"""
    if p(s().head):
        return lambda : cons(s().head, stream_filter(p, s().tail))
    else:
        return stream_filter(p, s().tail)

def stream_reduce(f, s, elem, p):
    """Takes a stream s, function f, starting point elem and predicate p
    and returns applying function to the first and second element,
    then outcome of this to the third, etc... until predicate p holds
     when feed with the next stream element. Example: Stream: natural numbers,
     function: +, starting element 0, predicate: > 4; result: 10,
     sum of natural numbers up to 4"""
    @tail_recursive
    def helper(f, stream, p, acc):
        if not p(stream().head):
            return acc
        else:
            return recurse(f, stream().tail, p, f(acc, stream().head))
    return helper(f, s, p, elem)

if __name__ == '__main__':
    lst = List_from_iter(list(range(9999)))
    print(lst)
    print(cons_map(lambda x: x * x, lst))
    print("filtered ", cons_filter(lambda x: not x % 2 == 0, cons_map(lambda x: x * x, lst)))
    print("fold_left", cons_reduce(add,cons_filter(lambda x: not x % 2 == 0, cons_map(lambda x: x * x, lst)) , 0))
    nat_numbers = make_stream(add, 1)
    nat_mapped = stream_map(lambda x: x * x, nat_numbers)
    nat_filtered = stream_filter(lambda x: not x % 2 == 0, nat_mapped)
    print(stream_reader(lambda x: x < 10, nat_numbers)) # -> (1 2 3 4 5 6 7 8 9)
    print(stream_reader(lambda x: x < 100, nat_mapped)) # -> (1 4 9 16 25 36 49 64 81)
    print(stream_reader(lambda x: x < 100, nat_filtered)) # -> (1 9 25 49 81)
    print(stream_reduce(add, nat_filtered, 0, lambda x: x <= 100)) # -> 165

