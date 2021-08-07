"""main

main module currelty two modes are supported -> interpreter and reading file - executing
"""

__author__ = "ales lerch"

import click
from src.interpret import Interpret

@click.command()
@click.option(
    "-i", "--inpt", help="Input file (if not specified than interpreter is on"
)
def main(inpt):
    Interpret(inpt).interpret()

if __name__ == "__main__":
    main()