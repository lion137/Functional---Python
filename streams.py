# Functional Python, streams, tests

# Part One: Thunks, and delaying evaluation

from immutable_lists import *

from operator import *


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

def bad_if(x, y, z):
    return x if y else z


def fact_bad(n):
    return bad_if(eq(n , 0), 1, n * fact_bad(n - 1))

# print(fact_bad(2))  # -> stack smashed

# How to change this function, how to tell her to evaluate all rght now (delaying evaluation)
# making function (high order function it calls function with zero args) form alrgs


def strange_if_works(x, y, z):
    return y(None) if x else z(None)


def fact_ok(n):
    return strange_if_works(eq(n, 0),
                            lambda _: 1,
                            lambda _: n * fact_ok(n - 1))

# print(fact_ok(50)) # -> works OK



z = lambda _: 1

# print((lambda _: 1)(None)) # -> 1

# delaying and force, we need a mutation (a little):


def delay(thunk):
    return [False, thunk]

# force will be called on the thing returns form delay


def force(p):
    if p[0]:
        return p[1]
    else:
        p[0] = True
        p[1] = p[1]()
        return p[1]

# streams, beginning

ones = lambda : cons(1, ones)  # stream of ones, ones returns a thunk: cons( 1, ones)
nat_numbers = make_stream(add, 1)

print("force tests", force(delay(nat_numbers)))


# print(ones().head) # -> 1

# print(ones().tail().head) # head of tail of stream, again 1

# stream of 1, 2, 3, 4, ...


f = lambda x: cons(x, lambda : f(x + 1))

#print(f(1)) # -> (1) list: 1, i jako Nil funkcja (thunk)

# stream of nats:

nat_numbers = lambda : f(1)
def nat_numbers_def():
    g = lambda x: cons(x, lambda: g(x + 1))
    return lambda : g(1)
nat_numbers = nat_numbers_def()
# print("type: ", type(nat_numbers()))
# print(nat_numbers().tail().tail().head) # -> 1 frst elem in stream

# print(nat_numbers().tail().head) # -> next number, 2

# powers of two stream:

f2 = lambda x: cons(x, lambda : f2(x * 2))

power_of_two = lambda : f2(1)


# print(nat_numbers().head) # -> 1
# print(nat_numbers().tail().head) # -> 2 ..
# print(nat_numbers().tail().tail().head)
# print(nat_numbers().tail().tail().tail().head)
# print(nat_numbers().tail().tail().tail().tail().head)
#
#
# print(power_of_two().head) # -> 1
# print(power_of_two().tail().head) # -> 2
# print(power_of_two().tail().tail().head) # -> 4...
# print(power_of_two().tail().tail().tail().head)
# print(power_of_two().tail().tail().tail().tail().head)


# stream maker..



# define natural numbers using the stream maker

nat_numbers_2 = make_stream(add, 1)

# print(nat_numbers_2().head) # -> 1
# print(nat_numbers_2().tail().head) # -> 2
# print(nat_numbers_2().tail().tail().head) # -> 3 ...

# powers of three:

powers_of_three = make_stream(mul, 3)
powers_of_two_2 = make_stream(mul, 2)


# print(powers_of_three().head) # -> 3
# print(powers_of_three().tail().head) # -> 9
# print(powers_of_three().tail().tail().head) # -> 27 ...

print("Using streams ------------------")

# define function which using a stream, numbers of
# evaluation in steram

def until(stream, test):
    """returns number of evaluation of stream
    before test"""
    @tail_recursive
    def f(stream, acc):
        tmp = stream()
        if test(tmp.head):
            return acc
        else:
            return recurse(tmp.tail, acc + 1)
    return f(stream, 1)


ones = lambda : cons(1, ones)

print(ones().tail().tail())

# 1, 2, 3, 4,...

f = lambda x: cons(x, lambda: f(x + 1))

nat_numbers = lambda: f(1)

nat_numbers().head # -> 1
nat_numbers().tail().head # -> 2

# nat numbers ver 2

def nat_numbers2():
    g = lambda x: cons(x, lambda: g(x + 1))
    return g(1)

nat_numbers2().head # -> 1
nat_numbers2().tail().head # -> 2 ...

stream_reader(lambda x: x < 10, nat_numbers2) # -> (1 2 3 4 5 6 7 8 9)



