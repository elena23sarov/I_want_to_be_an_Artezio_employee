"""UNIX cat command. Do the next things:
1. Display the contents of a file(s)      - cat filename1 filename2 ...
"""


def cat(f_arg, *args):
    """Display files' contents one by one."""
    if f_arg == 'cat':
        for arg in args:
            with open(arg, 'r+') as file_cont:
                print file_cont.read()

    else:
        print "Usage: cat <filename1> <filename2> ..."


def main():
    """Test cat() function."""
    cat('tac')
    cat('cat', 'links.txt')
    cat('cat', 'links.txt', 'another.py')


if __name__ == '__main__':
    main()
