"""UNIX cat command. Do the next things:
1. Display the contents of a file(s)      - cat filename1 filename2 ...
"""
import sys


def cat(*args):
    """Display files' contents one by one."""
    for arg in args:
        try:
            with open(arg, 'r+') as file_cont:
                print file_cont.read()
        except IOError as err:
            print err


def main():
    """Test cat() function."""
    args = sys.argv[1:]
    if not args:
        print "Usage: cat.py <filename1> <filename2> ..."
        sys.exit(1)

    cat(*args)


if __name__ == '__main__':
    main()
