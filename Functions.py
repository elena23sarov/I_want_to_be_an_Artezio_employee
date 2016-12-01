"""Functions - zip(), list comprehensions."""


def zip_list(*args):
    """Do the same as function zip() does."""
    zipped_lists = []
    min_len = min(len(arg) for arg in args)
    for j in range(min_len):
        elem = []
        for arg in args:
            elem.append(arg[j])
        zipped_lists.append(tuple(elem))
    return zipped_lists


def squares(my_list):
    """Return squares."""
    return [a**2 for a in my_list]


def seconds(my_list):
    """Return each second element."""
    return [a for a in my_list[1::2]]


def super_squares(my_list):
    """Return squares of even elements on odd positions."""
    return [a**2 for a in my_list[1::2] if a % 2 == 0]


print "Firstly, look on these list comprehensions. Input a list:"
while 1:
    try:
        X = map(int, raw_input().split())
        break
    except ValueError as err:
        print 'Please insert only numbers. ({})'.format(err)
print "Squares: \t", squares(X)
print "Each second elem: \t", seconds(X)
print "Squares of even elem in odd positions: \t", super_squares(X)
print "-"*20
print "Try zip() function. How many lists do you want to zip? (min = 2)"
LISTS_TO_ZIP = []
while 1:
    try:
        N = int(raw_input())
        if N > 1:
            break
        else:
            print "Zip function works for 2 or more lists. Try again"
    except ValueError as err:
        print 'Please insert only numbers. ({})'.format(err)
for i in range(N):
    print "Ok, insert list #{}:".format(i)
    while 1:
        try:
            Y = map(int, raw_input().split())
            break
        except ValueError as err:
            print 'Please insert only numbers. ({})'.format(err)
    LISTS_TO_ZIP.append(Y)
print zip_list(*LISTS_TO_ZIP)
