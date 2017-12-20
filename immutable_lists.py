# Cons lists, tail recursion decorator, functions on lists:

from _collections_abc import ABCMeta, abstractmethod


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



# immutable cons list and methods:
class Nil:
    """class Nil, the empty list"""

    def is_empty(self):
        return True

    def head(self):
        return Exception("Empty")

    def tail(self):
        return Exception("Empty")

    def get_next(self):
        return None

    def __str__(self):
        return "()"


class Cons:
    """Class cons, the non empty list: (head, list)"""

    def __init__(self, _head, _list_tail):
        self.head = _head
        self.tail = _list_tail

    def is_empty(self):
        return False

    def get_next(self):
        return self.tail

    def print_list(self):
            current = self
            out = ''
            out = str(current.head)
            # print(str(current.head))
            while not isinstance(current.tail, Nil):
                print("here", out)
                out += ' ' + str(current.head)
                current = current.tail
                print(str(current.head))
                print("here2", out)
            return '(' + out + ')'


class List(metaclass=ABCMeta):
    @abstractmethod
    def is_empty(self):
        pass

    def head(self):
        pass

    def tail(self):
        pass


List.register(Nil);
List.register(Cons)


@tail_recursive
def print_list(xs, out=''):
    current = xs
    out += ' ' + str(current.head)
    if isinstance(current.tail, Nil):
        print('(' + out + ')')
        return
    else:
        return recurse(xs.tail, out)


def create_list(args_list):
    """Crates immutable list from any indexable args"""
    tmp_list = cons(args_list[len(args_list) - 1], Nil())
    for x in range(len(args_list) - 2, -1, -1):
        tmp_list = cons(args_list[x], tmp_list)
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
    if empty(xs):
        return Exception("Out Of Bound")
    if n == 0:
        return xs.head
    else:
        return recurse(n - 1, xs.tail)


def empty(xs):
    if xs is Nil:
        return True
    else:
        return False


def cons(elem, xs):
    """Cons element elem to the list"""
    return Cons(elem, xs)

if __name__ == '__main__':
    x = cons(1, cons(2, Nil()))
    print_list(x)
    List = list(range(10000))
    imm_list = create_list(List)
    print_list(imm_list)
    print(nth(9999, imm_list))
    print(length(imm_list))