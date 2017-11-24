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

    def is_identificatior(self, val = ""):
        is_id = self.token.token_type == TokenType.identifier
        has_value = self.token.value == val
        return is_id and has_value if val else is_id

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
        elif self.is_identificatior("in"):
            self.next_token()
        elif self.is_identificatior():
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
        elif self.is_identificatior()\
                or self.is_identificatior("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            self.expression()
        else:
            self.error(f"Expected identificator, atom, (, = but {self.token} found")

    def expression(self):
        if self.is_identificatior()\
                or self.is_identificatior("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            self.value()
            self.expression_()
        else:
            self.error(f"Expected ( but {self.token} found")

    def expression_(self):
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
            self.error(f"Expected > or identifcator but {self.token} found")

    def value(self):
        if self.is_identificatior("fn"):
            self.next_token()
            self._lambda()
        elif self.is_identificatior():
            self.next_token()
        elif atomic_blonde():
            self.next_token()
        elif self.token.token_type == TokenType.left_paren:
            self.next_token()
            self.expression()
            if self.token == TokenType.right_paren:
                self.next_token()
            else:
                self.error(f"Expected ) but {self.token} found")
        elif self.token.token_type == TokenType.left_closed_braces:
            self.next_token()
            self.expression()
            if self.token == TokenType.right_closed_braces:
                self.next_token()
            else:
                self.error(f"Expected ) but {self.token} found")
        else:
            self.error(f"Expected ) but {self.token} found")

    def _lambda(self):
        if self.is_identificatior("fn"):
            self.next_token()
            self._lambda_()
        else:
            self.error(f"Expected ) but {self.token} found")

    def _lambda_(self):
        if self.is_identificatior():
            self.idens()
            self.x()
        else:
            self.error(f"Expected identifcator but {self.token} found")

    def idens(self):
        if is_identificatior():
            self.next_token()
            self.idens_()
        else:
            self.error(f"Expected identifcator but {self.token} found")

    def idens_(self):
        if self.token.token_type == TokenType.left_braces\
                or self.token.token_type == TokenType.arg_sep:
            self.token = None
        elif self.is_identificatior():
            self.next_token()
        else:
            self.error(f"Expected identifcator but {self.token} found")

    def x(self):
        if self.token.token_type == TokenType.arg_sep:
            self.next_token()
            self.expression()
        elif self.token.token_type == TokenType.left_braces:
            self.body()
        else:
            self.error(f"Expected identifcator but {self.token} found")

    def body(self):
        if self.token.token_type == TokenType.left_braces:
            self.next_token()
            self.binding_list()
            if self.is_identificatior("in"):
                self.next_token()
                self.expression()
            else:
                self.error(f"Expected in but {self.token} found")
            if self.token.token_type == TokenType.right_braces:
                self.next_token()
            else:
                self.error(f'{{ {"10"}')
                self.error(f'Expected }} but {self.token} found')
        else:
            self.error(f"Expected {{ but {self.token} found")


if __name__ == '__main__':
    t = Token()
    p = Parser(t.lexer())
    print(p.program())

