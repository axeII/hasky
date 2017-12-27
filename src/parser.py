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

from sys import exit, stderr, stdin, stdout
from lexer import Token, TokenType
from ast import Function, CallingFunction, Number, String, Assigment, Variable, Real

class Parser:

    def __init__(self, lexer):
        self.token = None
        self.ignore = False
        self.root_ast = []
        self.lexer = lexer
        self.next_token()

    def next_token(self):
        try:
            self.token = next(self.lexer)
            #print(self.token.token_type, self.token.value)#DEBUGGING
            return True
        except (StopIteration, AttributeError):
            return False

    def error(self, exp):
        print(f"On line: {self.token.line} expected identifier but {self.token.token_value} found")
        exit(2)

    def atomic_blonde(self):
        """checks if current token - self.token is atom -> is in string, real or integer type"""
        return self.token.token_type in (TokenType.string, TokenType.real, TokenType.integer)


    def is_identifier(self, val=""):
        is_id = self.token.token_type == TokenType.identifier
        has_value = self.token.token_value == val
        return is_id and has_value if val else is_id

    def program(self):
        #print("Program")
        if self.is_identifier():
            self.binding_list()
        elif self.token.token_type == TokenType.end_of_file:
            print("[Error] No input was probably set.")
            return 1
        elif self.token.token_value == '\\n':
            pass
        else:
            self.error("identifier")
        return 0

    def binding_list(self):
        #print("binding_list")
        if self.is_identifier():
            self.single_binding()
            self.binding_list_()
        else:
            self.error("identifier")

    def binding_list_(self):
        #print("binding_list_")
        if self.token.token_type == TokenType.end_of_file:
            self.token = None
        elif self.is_identifier("in"):
            self.next_token()
        elif self.is_identifier():
            self.binding_list()
        elif self.token.token_value == '\\n':
            #for debugging
            self.token = None
        else:
            self.error("identifier, newline, fn, eof")

    def single_binding(self):
        #print("single_binding")
        if self.is_identifier():
            self.id = self.token
            self.next_token()
            self.single_binding_()
        else:
            self.error(f"Expected identifier but {self.token} found")
            self.error("identifier")

    def single_binding_(self):
        #print("single_binding_")
        if self.token.token_type == TokenType.assigment_op:
            self.next_token()
            #self.expression()
            self.root_ast.append(Assigment(self.id, self.expression()))
        elif self.is_identifier()\
                or self.is_identifier("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            self.root_ast.append(CallingFunction(self.id, self.expression()))
        else:
            self.error("identifier, atom, (, =")

    def expression(self):
        #print("expression")
        if self.is_identifier()\
                or self.is_identifier("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            val = [self.value()]
            rest = self.expression_()
            return val + rest
        else:
            self.error("(")

    def expression_(self):
        #print("expression_")
        if self.token.token_type == TokenType.separator:
            if not self.ignore:
                self.next_token()
            self.ignore = False
            return list()
        elif self.is_identifier()\
                or self.is_identifier("fn")\
                or self.atomic_blonde()\
                or self.token.token_type == TokenType.left_paren\
                or self.token.token_type == TokenType.left_closed_braces:
            return self.expression()
        elif self.token.token_type == TokenType.fn_conj:
            self.next_token()
            self.expression()
            #should return something?
        else:
            self.error("identifier, >")

    def value(self):
        #print("value")
        if self.is_identifier("fn"):
            return self._lambda()
        elif self.is_identifier():
            val = self.token
            self.next_token()
            return Variable(val)
        elif self.atomic_blonde():
            if self.token.token_type == TokenType.string:
                val = String(self.token)
            elif self.token.token_type == TokenType.integer:
                val = Number(self.token)
            else:
                val = Real(self.token)
            self.next_token()
            return val
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
        #print("_lambda")
        if self.is_identifier("fn"):
            self.next_token()
            return self._lambda_()
        else:
            self.error(")")

    def _lambda_(self):
        #print("_lambda_")
        if self.is_identifier():
            #print(self.idens())
            #print(self.x())
            return Function(self.id, self.idens(), self.x())
        else:
            self.error("identifier")

    def idens(self):
        #print("idens")
        if self.is_identifier():
            args = [self.token]
            self.next_token()
            return args + self.idens_()
        else:
            self.error("identifier")

    def idens_(self):
        #print("idens_")
        if self.token.token_type == TokenType.left_braces\
                or self.token.token_type == TokenType.arg_sep:
            return list()
            #self.token = None
        elif self.is_identifier():
            args = [self.token]
            self.next_token()
            try:
                return args + self.idens_()
            except TypeError:
                return args
        else:
            self.error("identifier")

    def x(self):
        #print("x")
        if self.token.token_type == TokenType.arg_sep:
            self.next_token()
            self.ignore = True
            return self.expression()
        elif self.token.token_type == TokenType.left_braces:
            self.body()
        else:
            self.error("identifier")

    def body(self):
        #print("body")
        if self.token.token_type == TokenType.left_braces:
            self.next_token()
            self.binding_list()
            if self.is_identifier("in"):
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

