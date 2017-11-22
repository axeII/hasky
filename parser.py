"""Parser

Syntactic analyzator for discovering grammar

Current grammar:
Program -> BL
BL -> SB BL'
BL' -> epsilon | ; BL | '\n' BL
SB -> id SB'
SB' -> = Expr | Expr
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

from lexer import *
from sys import exit, stderr, stdin, stdout

class Parser:

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
        print(msg, file = stderr)
        exit(2)

    def atomic_blonde(self):
        # add boolean?
        # is atomic
        return self.token.token_type in (TokenType.string, TokenType.real, TokenType.integer)

    def is_identificatior(self):
        return self.token.token_type == TokenType.identifier

    def fn_keyword(self):
        return self.token.token_type == TokenType.identifier and self.token.value == "fn"

    #Program -> BL
    def program(self):
        if self.is_identificatior():
            self.binding_list()
        elif self.token.token_type == TokenType.end_of_file:
            pass
        else:
            self.error(f"Expected identificator but {self.token} found")

    #BL → SB BL'
    def binding_list(self):
        if self.is_identificatior():
            self.single_binding()
            self.single_binding_()
        else:
            self.error(f"Expected identificator but {self.token} found")

    #BL' -> epsilon | ; BL | '\n' BL
    def binding_list_(self):
        if self.token.token_type == TokenType.end_of_file:
            self.token = None
        elif self.fn_keyword():
            self.next_token()
        elif self.token.token_type == TokenType.semicolon or\
                self.token.token_type == TokenType.line_feed:
            self.next_token()
            self.binding_list()
        else:
            self.error(f"Expected ;, new line, fn,end of file but {self.token} found")

    def single_binding(self):
        if self.is_identificatior():
            self.next_token()
            self.single_binding_()
        else:
            self.error(f"Expected identificator but {self.token} found")

    def single_binding_(self):
        if self.token.token_type == TokenType.assigment_op:
            self.next_token()
            self.expression()
        elif self.is_identificatior or self.atomic_blonde()\
                or self.token.token_type == tokentype.left_paren:
            self.expression()
        else:
            self.error(f"Expected identificator, atom, (, = but {self.token} found")

    def expression(self):
        if self.is_identificatior or self.atomic_blonde()\
                or self.token.token_type == tokentype.left_paren:
            self.value()
            self.expression_()
        else:
            self.error(f"Expected ( but {self.token} found")

    def expression_(self):
        if self.token.token_type == TokenType.end_of_file:
            self.token = None
        elif self.fn_keyword() or atomic_blonde() or is_identificatior():
            self.next_token()

if __name__ == '__main__':
    t = Token()
    p = Parser(t.lexer())
    print(p.program())


