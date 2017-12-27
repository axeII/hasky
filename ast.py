"""AST

AST tree for data sctructure of grammar data
"""

__author__ = 'ales lerch'

from lexer import TokenType

class AST:

    def __init__(self, value, name):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def _eval(self):
        if self.value.token_type == TokenType.string:
            return f'"{self.value.token_value}"'
        elif self.value.token_type == TokenType.integer:
            return int(self.value.token_value)
        else:
            return self.value.token_value


class Variable(AST):

    def __init__(self, value):
        super().__init__(value, "Variable")

class Number(AST):

    def __init__(self, value):
        super().__init__(value, "Number")

class Real(AST):

    def __init__(self, value):
        super().__init__(value, "Real")

class String(AST):

    def __init__(self, value):
        super().__init__(value, "String")

class Assigment(AST):

    def __init__(self, keyword, value):
        super().__init__(value, "Assigment")
        self.keyword = keyword

class Function(AST):

    def __init__(self, keyword, args, body):
        super().__init__(body, "Function")
        self.args = args
        self.keyword = keyword

class CallingFunction(AST):
    def __init__(self, keyword, args):
        super().__init__(args, "CallingFunction")
        self.keyword = keyword

def ast_value(data):
    if isinstance(data, AST):
        return data.value
    else:
        return data

