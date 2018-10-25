from sys import stderr


def perror(*args, **kwargs):
    print(*args, file=stderr, **kwargs)
