"""Lexer

Lexical analyzator for discovering states
"""
__author__ = "ales lerch"

import itertools
import re
from enum import Enum
from sys import exit, stdin


class LexerState(Enum):
    Q_S = 0
    Q_A1 = 1
    Q_AF = 2
    Q_B1 = 3
    Q_B2 = 4
    Q_B1F = 5
    Q_B2F = 6
    Q_C1 = 7
    Q_D1 = 8
    Q_D2 = 9
    Q_F = 10


class TokenType(Enum):
    identifier = 0
    integer = 1
    string = 2
    left_paren = 3  # (
    right_paren = 4  # )
    left_braces = 5  # {
    right_braces = 6  # }
    left_closed_braces = 7  # [
    right_closed_braces = 8  # ]
    separator = 9
    tab = 10
    space = 11
    comma = 12  # ,
    arg_sep = 13  #:
    fn_conj = 14  # >
    assigment_op = 15  # =
    dot = 16  # .
    real = 17
    end_of_file = 18


class Stream:
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        # print(self.data)
        return self.data

    def __exit__(self, exception_type, exception_value, traceback):
        pass


class Token:
    def __init__(self, line=1, token_value="", token_type=None):
        self.line = line
        self.token_value = token_value
        self.token_type = token_type
        # think about splitting input text for parts

    def __repr__(self):
        return f"Token::<line: {self.line}, type: {self.token_type}, value: {self.token_value}>"

    def check_input(self, input_file, text):
        if input_file:
            with open(input_file) as f:
                read_data = f.readlines()
            return Stream(read_data)
        elif text:
            return Stream([text])
        else:
            return stdin

    def lexer(self, text="", input_file=""):
        last_line_number = 1
        id_number_free = re.compile("[a-zA-Z+\-\/\*_]+")
        id_complex = re.compile("[a-zA-Z0-9_+\-\/\*']+")
        universal = re.compile("[,:>=\.\[\]]+")
        input_file = self.check_input(input_file, text)
        with input_file as content:
            for line, line_number in zip(content, itertools.count(1)):
                value = ""
                state = LexerState.Q_S
                last_line_number = line_number
                while line != "":
                    if state == LexerState.Q_S:
                        if id_number_free.match(line[0]):
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_A1
                        elif line[0] == '"':
                            line = line[1:]
                            state = LexerState.Q_D1
                        elif line[0] in ("+", "-") or line[0].isdigit():
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_B1
                        elif line[0] == "#":
                            line = line[1:]
                            state = LexerState.Q_C1
                        elif line[0] == "(":
                            line = line[1:]
                            yield Token(last_line_number, "(", TokenType.left_paren)
                        elif line[0] == ")":
                            line = line[1:]
                            yield Token(last_line_number, ")", TokenType.right_paren)
                        elif line[0] == "{":
                            line = line[1:]
                            yield Token(last_line_number, "{", TokenType.left_braces)
                        elif line[0] == "}":
                            line = line[1:]
                            yield Token(last_line_number, "}", TokenType.right_braces)
                        elif line[0] == ",":
                            line = line[1:]
                            yield Token(last_line_number, ",", TokenType.comma)
                        elif line[0] == ":":
                            line = line[1:]
                            yield Token(last_line_number, ":", TokenType.arg_sep)
                        elif line[0] == ">":
                            line = line[1:]
                            yield Token(last_line_number, ">", TokenType.fn_conj)
                        elif line[0] == "=":
                            line = line[1:]
                            yield Token(last_line_number, "=", TokenType.assigment_op)
                        elif line[0] == ";":
                            line = line[1:]
                            yield Token(last_line_number, ";", TokenType.separator)
                        elif line[0] == "\n":
                            line = line[1:]
                            yield Token(last_line_number, "\\n", TokenType.separator)
                        elif line[0] == " " or line[0] == "\t":
                            line = line[1:]
                        elif line[0] == ".":
                            line = line[1:]
                            yield Token(last_line_number, ".", TokenType.dot)
                        else:
                            print(
                                f"[Error][LA] found uknown character {line[0]}, {state}"
                            )
                            exit(1)

                    elif state == LexerState.Q_A1:
                        if id_number_free.match(line[0]) or id_complex.match(line[0]):
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_AF
                        else:
                            yield Token(last_line_number, value, TokenType.identifier)
                            value = ""
                            state = LexerState.Q_S
                            # print(f"[Error][LA] found uknown character {line[0]} {state}")
                            # exit(1)

                    elif state == LexerState.Q_AF:
                        if id_number_free.match(line[0]) or id_complex.match(line[0]):
                            value += line[0]
                            line = line[1:]
                        else:
                            yield Token(last_line_number, value, TokenType.identifier)
                            value = ""
                            state = LexerState.Q_S

                    elif state == LexerState.Q_B1:
                        if line[0].isdigit():
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_B1F
                        elif line[0] in ("e", "E", "."):
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_B2
                        else:
                            yield Token(
                                last_line_number, float(value), TokenType.integer
                            )
                            value = ""
                            state = LexerState.Q_S
                            # print(f"[Error][LA] found uknown character {line[0]} {state}")
                            # exit(1)

                    elif state == LexerState.Q_B1F:
                        if line[0].isdigit():
                            value += line[0]
                            line = line[1:]
                        elif line[0] in ("e", "E", "."):
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_B2
                        else:
                            yield Token(
                                last_line_number, float(value), TokenType.integer
                            )
                            value = ""
                            state = LexerState.Q_S

                    elif state == LexerState.Q_B2:
                        if line[0].isdigit():
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_B2F
                        else:
                            print(
                                f"[Error][LA] found uknown character {line[0]} {state}"
                            )
                            exit(1)

                    elif state == LexerState.Q_B2F:
                        if line[0].isdigit():
                            value += line[0]
                            line = line[1:]
                        else:
                            yield Token(last_line_number, float(value), TokenType.real)
                            value = ""
                            state = LexerState.Q_S

                    elif state == LexerState.Q_C1:
                        if (
                            line[0] in ("\t", " ")
                            or universal.match(line[0])
                            or id_complex.match(line[0])
                        ):
                            line = line[1:]
                        elif line[0] == "\n":
                            line = line[1:]
                            value = ""
                            state = LexerState.Q_S
                        else:
                            print(
                                f"[Error][LA] found uknown character {line[0]} {state}"
                            )
                            exit(1)

                    elif state == LexerState.Q_D1:
                        if (
                            line[0] in ("\\", "\t", " ")
                            or universal.match(line[0])
                            or id_complex.match(line[0])
                        ):
                            value += line[0]
                            line = line[1:]
                            status = LexerState.Q_D2
                        elif line[0] == '"':
                            yield Token(last_line_number, str(value), TokenType.string)
                            value = ""
                            line = line[1:]
                            state = LexerState.Q_S
                        else:
                            print(
                                f"[Error][LA] found uknown character line:'{line[0]}' state:{state}"
                            )
                            exit(1)

                    elif state == LexerState.Q_D2:
                        if (
                            line[0] in ("\\", '"', "\t", " ")
                            or universal.match(line[0])
                            or id_complex.match(line[0])
                        ):
                            value += line[0]
                            line = line[1:]
                            state = LexerState.Q_D1
                        else:
                            print(
                                f"[Error][LA] found uknown character {line[0]} {state}"
                            )
                            exit(1)
                if value != "":
                    if state == LexerState.Q_A1:
                        yield Token(line_number, value, TokenType.identifier)
                    elif state == LexerState.Q_B1:
                        yield Token(line_number, float(value), TokenType.integer)
                    else:
                        print("[Warning][LA] Some data has not been checked by LA:")
                        print(value)
        yield Token(last_line_number, "EOF", TokenType.end_of_file)


if __name__ == "__main__":
    t = Token()
    for i in t.lexer():
        print(i)
