"""Desktop daemon

This is desktop deamon for checking desktop files
"""
__author__ = 'ales lerch'

import re
from sys import stdin
from enum import Enum

class LexerState(Enum):
    Q_S = 0
    A1 = 1
    AF = 2
    B1 = 3
    B2 = 4
    B1F = 5
    B2F = 6
    C1 = 7
    D1 = 8
    D2 = 9
    F = 10


class TokenType(Enum):
    identifier = 0
    number = 1
    string = 2
    left_paren = 3
    right_paren = 4
    left_braces = 5
    right_braces = 6
    left_closed_braces = 7
    right_closed_braces = 8
    new_line = 9
    tab = 10
    space = 11
    comma = 12
    arg_sep = 13
    fn_conj = 14
    assigment_op = 15
    dot = 16
    expr_sperator = 17
    end_of_file = 18


class Token:

    def __init__(self, line, value, token_type):
        self.line = line
        self.value = value
        self.token_type = token_type
        #think about splitting input text for parts

    def __repr__(self):
        return f"[line: {self.line}, type: {self.token_type}] {self.value}"

    def lexer(self, input_file = stdin):
        last_line_nuber = 0
        id_number_free = re.compile("[a-zA-Z_-]+-")
        id_complex = re.compile("[a-zA-Z0-9_+-]+")
        with open(input_file) as content:
            for line, line_number in zip(content, itertools.count()):
                value = ""
                state = LexerState.q_s
                last_line_nuber = line_number
                while line != "":
                    if state == LexerState.Q_S:
                        if id_number_free.match(line[0]):
                            value += line[0]
                            line = lien[1:]
                            state = LexerState.A1
                        elif line[0] == '"':
                            line = line[1:]
                            state = LexerState.D1
                        elif line[0] in ('+','-') or line[0].isdigit():
                            value += line[0]
                            line = line[1:]
                            state = LexerState.B1
                        elif line[0] == '#':
                            line = line[1:]
                            state  = LexerState.C1
                        elif line[0] == '(':
                            line = line[1:]
                            yield Token(last_line_nuber,'(',TokenType.left_paren)
                        elif line[0] == ')':
                            line = line[1:]
                            yield Token(last_line_nuber,')',TokenType.right_paren)
                        elif line[0] == '{':
                            line = line[1:]
                            yield Token(last_line_nuber,'{',TokenType.left_braces)
                        elif line[0] == '}':
                            line = line[1:]
                            yield Token(last_line_nuber,'}',TokenType.right_braces)
                        elif line[0] == ',':
                            line = line[1:]
                            yield Token(last_line_nuber,',',TokenType.comma)
                        elif line[0] == ':':
                            line = line[1:]
                            yield Token(last_line_nuber,':',TokenType.arg_sep)
                        elif line[0] == '>':
                            line = line[1:]
                            yield Token(last_line_nuber,'>',TokenType.fn_conj)
                        elif line[0] == '=':
                            line = line[1:]
                            yield Token(last_line_nuber,'=',TokenType.assigment_op)
                        elif line[0] == ';':
                            line = line[1:]
                            yield Token(last_line_nuber,';',TokenType.expr_sperator)
                        elif line[0] == '\n':
                            line = line[1:]
                            yield Token(last_line_nuber,'\n',TokenType.expr_sperator)
                        elif line[0] == ' ':
                            line = line[1:]
                            yield Token(last_line_nuber,' ',TokenType.space)
                        elif line[0] == '.':
                            line = line[1:]
                            yield Token(last_line_nuber,'.',TokenType.dot)

                    elif state == LexerState.A1:
                        if id_number_free.match(line[0]) or id_complex.match(line[0]):
                            value += line[0]
                        else:
                            pass

        yield Token(last_line_number, "EOF", TokenType.end_of_file)

if __name__ == "__main__":
    t = Token(0,'',TokenType.space)
