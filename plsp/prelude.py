def drop(n, xs):
    '''(drop n xs)
    Returns a new list without the first n elements.
    '''
    return xs[n:]


def take(n, xs):
    '''(take n xs)
    Returns the n first elements of the list xs.
    '''
    return xs[0:n]


def comp(*fs):
    '''(comp) (comp f1) (comp f1 f2 ...)
    Returns a function that is the composition of the functions given as arguments.
    '''
    rev = fs[::-1]
    def f(x):
        return reduce(lambda x, f: f(x), rev, x)
    return f


def first(xs):
    '''(first xs)
    Returns the first element of the list.
    '''
    return xs[0]


def cons(x, xs):
    '''(cons x xs)
    Returns a new list with the first item is x and the tail is xs.
    '''
    return [x] + xs


def doc(f):
    '''(doc f)
    Prints the module and the documentation of a function.
    '''
    print f.__module__ + '.' + f.__name__
    print f.__doc__

def id(x):
    '''(id x)
    The identity function. It just returns x.
    '''
    return x

def partial(f, *args):
    '''(partial f x1 x2 ...)
'''
    def inner(*rest):
        return f(*(args + rest))
    return inner


def splat():
    pass
