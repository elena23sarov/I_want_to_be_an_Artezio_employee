""" Generators:
1 - infinite generator
2 - xrange()
3 - string generator
"""
import re
import string
import random


def infinite():
    """Return promise to be with you in an infinite loop."""
    while 1:
        yield "I'll forever be with you"


def my_xrange(start, stop='', step=1):
    """Do the same as xrange() function."""
    if stop == '':
        for value in range(start):
            yield value
    else:
        for value in range(start, stop, step):
            yield value


def random_string(size, chars=string.digits + string.letters):
    """Return strings of random length and random alphanumeric symbols."""
    yield ''.join(random.choice(chars) for _ in range(size))


def str_validator(amount, length, nums=1):
    """Return valid strings."""
    while amount > 0:
        for rand_str in random_string(length):
            fact_nums = 0
            for char in rand_str:
                if char.isdigit():
                    fact_nums += 1
            if fact_nums == nums:
                yield rand_str
                amount -= 1


print "Hello. We have several options. \n" \
      "1) To see an 'infinite generator', please type --infinite \n" \
      "or print anything other / nothing to skip"
if raw_input().startswith('--infinite'):
    for i in infinite():
        print i
print '2) Look on xrange() in action. Usage: xrange(start, stop, step)'
INP = raw_input()
if INP.startswith('xrange'):
    MATCH = re.search(r'(?<=\()(-*\d*),* *(-*\d*),* *(-*\d*)(?=\))', INP)
    START = int(MATCH.group(1))
    if MATCH.group(2) and MATCH.group(3):
        STOP, STEP = int(MATCH.group(2)), int(MATCH.group(3))
        for i in my_xrange(START, STOP, STEP):
            print i
    elif MATCH.group(2):
        STOP = int(MATCH.group(2))
        for i in my_xrange(START, STOP):
            print i
    else:
        for i in my_xrange(START):
            print i
else:
    print "Sorry, we have no such a function"

print '3) You can get random strings with rand_str() function \n' \
      'Usage: rand_str(amount, length, nums) //nums = numbers in a string'
INP = raw_input()
if INP.startswith('rand_str'):
    MATCH = re.search(r'(?<=\()(\d*),* *(\d*),* *(\d*)(?=\))', INP)
    if not MATCH:
        print "--ExecutionError-- function should get numeric arguments"
    elif not MATCH.group():
        print "--ExecutionError-- function should get 1 to 3 arguments"
    else:
        AMOUNT = int(MATCH.group(1))
        if MATCH.group(2) and MATCH.group(3):
            LENGTH, NUMS = int(MATCH.group(2)), int(MATCH.group(3))
        elif MATCH.group(2):
            LENGTH, NUMS = int(MATCH.group(2)), -1
        else:
            LENGTH, NUMS = random.randint(1, 60), -1
        if NUMS != -1:
            for i in str_validator(AMOUNT, LENGTH, NUMS):
                print i
        else:
            for i in str_validator(AMOUNT, LENGTH):
                print i
else:
    print "Sorry, we have no such a function"
