def memoize(f):
    cache = {}
    def memoized_function(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    return memoized_function