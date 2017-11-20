"""Parser

Syntactic analyzator for discovering grammar

Current grammar:
Program -> BL
BL -> SB BL'
BL' -> epsilon | ; BL | '\n' BL
SB -> id = Expr | id Expr
Expr -> Val Expr'
Expr' -> epsilon| Expr | > Expr
Val -> id | atom | Lambda | ( Expr) | Let | [Expr] | .[Expr]
Lambda -> fn Lambda'
Lambda' -> Iden : Expr | Iden Let'
Iden -> id Iden'
Iden' -> epsilon | id Iden'
Let' -> { BL in Expr }
"""
__author__ = 'ales lerch'

from sys import exit
from lexer import *

class Parse:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = None
        self.next_token()


    def next_token(self):
        try:
            self.token = next(self.lexer)
            return True
        except StopIteration:
            return False

    def error(self, msg = ""):
        print(msg, file = sys.stderr)
        sys.exit(2)

    def is_atom(self):
        return self.token.token_type in (TokenType.string, TokenType.real, TokenType.integer)

