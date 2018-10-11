from sys import stderr


def debug_print(*args, **kwargs):
    print(*args, **kwargs, file=stderr)

