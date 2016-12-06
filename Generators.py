""" Generators:
1 - infinite generator
2 - xrange()
3 - string generator
"""
import string
import random


def infinite():
    """Return promise to be with you in an infinite loop."""
    while 1:
        yield "I'll forever be with you"


def my_xrange(start, stop=None, step=1):
    """Do the same as xrange() function."""
    if stop is None:
        for value in range(start):
            yield value
    else:
        for value in range(start, stop, step):
            yield value


def random_string(size, chars=string.digits + string.letters):
    """Return strings of random length and random alphanumeric symbols."""
    yield ''.join(random.choice(chars) for _ in range(size))


def str_validator(amount=None, length=None, nums=1):
    """Return valid strings."""
    if amount is not None:
        if length is None:
            length = random.randint(nums, 60)
        if length >= nums:
            while amount > 0:
                for rand_str in random_string(length):
                    fact_nums = 0
                    for char in rand_str:
                        fact_nums += 1 if char.isdigit() else 0
                    if fact_nums == nums:
                        yield rand_str
                        amount -= 1
        else:
            print "--ExecutionError-- length can't be less than nums"
    else:
        print "--ExecutionError-- function should get 1 to 3 arguments"


def main():
    """Test my_xrange and str_validator."""
    assert list(my_xrange(1, 5, 2)) == list(xrange(1, 5, 2))
    assert list(my_xrange(5)) == list(xrange(5))
    assert list(my_xrange(5, 0, -1)) == list(xrange(5, 0, -1))
    assert list(my_xrange(-5, 5)) == list(xrange(-5, 5))
    for i in str_validator():
        print i
    print '-----'
    for i in str_validator(4):
        print i
    print '-----'
    for i in str_validator(2, 5):
        print i
    print '-----'
    for i in str_validator(2, 10, 3):
        print i
    print '-----'
    for i in str_validator(3, 4, 5):
        print i
    print ''


if __name__ == "__main__":
    main()
