"""AST

AST tree for data sctructure of grammar data
"""

__author__ = 'ales lerch'
"""
class Node:

    def __init__(self, name, predict, data):
        self.name = name
        self.data = data
        self.predicator = predict
        self.sub_followers = []

class AST:

    def __init__(self):
        self.root = None
        self.pointer = None

    def add_node(self, new_n_data, new_key, key):
        self.pointer = self.search_ast(key)
        self.pointer.sub_followers.append(Node(new_key, key, new_n_data))#new_data.key

    def get_node(self, key):
        return self.search_ast(key).data

    def search_ast(self, key):
        visited = []
        stack = [self.root]
        while stack:
            current = stack.pop()
            if current.name == key:
                return current
            visited.append(current)
            for next_ in list(filter(lambda x: x not in visited, current.sub_followers)):
                stack.append(next_)
        return None #exception? or empty Node?"""


class AST:

    def __init__(self, value, name):
        self.name = name
        self.value = value

    def _eval(self):
        return self.value.value

class Variable(AST):

    def __init__(self, value):
        super().__init__(value, "Number")

class Number(AST):

    def __init__(self, value):
        super().__init__(value, "Number")

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

