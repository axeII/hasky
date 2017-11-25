"""Parser

Syntactic analyzator for discovering grammar

Current grammar:
Program -> BL
BL -> SB BL'
BL' -> EPSILON | BL
SB -> id SB'
SB' -> = Expr | Expr
Expr -> Val Expr'
Expr' -> s | Expr | > Expr
Val -> id | atom | Lambda | ( Expr ) | [ Expr ]
Lambda -> fn Lambda'
Lambda' -> Iden X
X -> : Expr | Body
Iden -> id Iden'
Iden' -> EPSILON | id Iden'
Body -> { BL in Expr }
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
            print(self.token.token_type, self.token.value)
            return True
        except StopIteration:
            return False

    def error(self, exp):
        print(f"On line: {self.token.line} expected identificator but {self.token.value} found")
        exit(2)

    def atomic_blonde(self):
        # add boolean?
        # is atomic
        return self.token.token_type in (TokenType.string, TokenType.real, TokenType.integer)

    def is_identificatior(self, val = ""):
        is_id = self.token.token_type == TokenType.identifier
        has_value = self.token.value == val
        return is_id and has_value if val else is_id

    #Program -> BL
    def program(self):
        print("Program")
        if self.is_identificatior():
            self.binding_list()
        elif self.token.token_type == TokenType.end_of_file:
            pass
        else:
            self.error("identificator")

    #BL → SB BL'
    def binding_list(self):
        print("binding_list")
        if self.is_identificatior():
            self.single_binding()
            self.binding_list_()
        else:
            self.error("identificator")

    #BL' -> epsilon | ; BL | '\n' BL
    def binding_list_(self):
        print("binding_list_")
        if self.token.token_type == TokenType.end_of_file:
            self.token = None
        elif self.is_identificatior("in"):
            self.next_token()
        elif self.is_identificatior():
            self.binding_list()
        else:
            self.error("identificator, newline, fn, eof")

    def single_binding(self):
        print("single_binding")
        if self.is_identificatior():
            self.next_token()
            self.single_binding_()
        else:
            self.error(f"Expected identificator but {self.token} found")
            self.error("identificator")

    def single_binding_(self):
        print("single_binding_")
        if self.token.token_type == TokenType.assigment_op:
            self.next_token()
            self.expression()
        elif self.is_identificatior()\
                or self.is_identificatior("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            self.expression()
        else:
            self.error("identificator, atom, (, =")

    def expression(self):
        print("expression")
        if self.is_identificatior()\
                or self.is_identificatior("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            self.value()
            self.expression_()
        else:
            self.error("(")

    def expression_(self):
        print("expression_")
        if self.token.token_type == TokenType.separator:
            self.next_token()
        elif self.is_identificatior()\
                or self.is_identificatior("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            self.expression()
        elif self.token.token_type == TokenType.fn_conj:
            self.next_token()
            self.expression()
        else:
            self.error("identificator, >")

    def value(self):
        print("value")
        if self.is_identificatior("fn"):
            self._lambda()
        elif self.is_identificatior():
            self.next_token()
        elif self.atomic_blonde():
            self.next_token()
        elif self.token.token_type == TokenType.left_paren:
            self.next_token()
            self.expression()
            if self.token == TokenType.right_paren:
                self.next_token()
            else:
                self.error(")")
        elif self.token.token_type == TokenType.left_closed_braces:
            self.next_token()
            self.expression()
            if self.token == TokenType.right_closed_braces:
                self.next_token()
            else:
                self.error(")")
        else:
            self.error(")")

    def _lambda(self):
        print("_lambda")
        if self.is_identificatior("fn"):
            self.next_token()
            self._lambda_()
        else:
            self.error(")")

    def _lambda_(self):
        print("_lambda_")
        if self.is_identificatior():
            self.idens()
            self.x()
        else:
            self.error("identificator")

    def idens(self):
        print("idens")
        if self.is_identificatior():
            self.next_token()
            self.idens_()
        else:
            self.error("identificator")

    def idens_(self):
        print("idens_")
        if self.token.token_type == TokenType.left_braces\
                or self.token.token_type == TokenType.arg_sep:
            self.token = None
        elif self.is_identificatior():
            self.next_token()
        else:
            self.error("identificator")

    def x(self):
        print("x")
        if self.token.token_type == TokenType.arg_sep:
            self.next_token()
            self.expression()
        elif self.token.token_type == TokenType.left_braces:
            self.body()
        else:
            self.error("identificator")

    def body(self):
        print("body")
        if self.token.token_type == TokenType.left_braces:
            self.next_token()
            self.binding_list()
            if self.is_identificatior("in"):
                self.next_token()
                self.expression()
            else:
                self.error("in")
            if self.token.token_type == TokenType.right_braces:
                self.next_token()
            else:
                self.error("}}")
        else:
            self.error("{{")

if __name__ == '__main__':
    t = Token()
    p = Parser(t.lexer())
    print(p.program())

