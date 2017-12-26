"""main

main module currelty two modes are supported -> interpreter and reading file - executing
"""

__author__ = 'ales lerch'

from interpret import *
from sys import argv

if __name__ == '__main__':
    if len(argv) == 1:
        Interpret(None, True).interpret()
    else:
        Interpret(argv[1], False).interpret()

