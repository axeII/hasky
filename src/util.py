"""Util

utils separated into module util, used for project
"""
__author__ = "ales lerch"

from ast import AST

from src.lexer import Token


class ContextValue:

    __slots__ = ("cont_val_type", "cont_val_data")

    def __init__(self, type_, data):
        self.cont_val_type = type_
        if isinstance(data, list):
            self.cont_val_data = data[0]
        else:
            self.cont_val_data = data

    def eval_cvalue(self):
        return self.cont_val_data._eval()


class FunctionNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class DiffenrentTypes(Exception):
    def __init__(self, message):
        super().__init__(message)


def untoken(test_token):
    if isinstance(test_token, Token):
        return test_token.token_value
    else:
        return test_token


def ast_value(data):
    if isinstance(data, AST):
        return data.value
    else:
        return data
