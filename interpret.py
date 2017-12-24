"""Parser

Syntactic analyzator for discovering grammar

"""
__author__ = 'ales lerch'

#import uuid
from ast import *
from lexer import *
from parser import Parser

class Interpret:

    def __init__(self, on_interpreter = False):
        self.token = Token()
        self.parser = None
        #self.context = {}
        self.init_context()
        if on_interpreter:
            while True:
                try:
                    text_ = input('flang> ')
                except EOFError:
                    break
                if not text_:
                    continue

                lexer = self.token.lexer(text=text_)
                parser = Parser(lexer)
                return_value = parser.program()
                ast = parser.root_ast
                self.interpret(ast)
        else:
            self.parser = Parser(self.token.lexer())

    def init_context(self):
        self.context = {
                "eval_id": { "type": Function("Function", None, None),"data": Function("eval", None,
                    lambda x: self.context[x.value]["data"]._eval())},
                #"eval2": map(lambda x: self.context[x.value] = x._eval(), arguments)
                }

    def interpret(self, data = None):

        def search_function(name_of_function):
            for each in list(filter(lambda x: x["type"].name != "CallingFunction",self.context.values())):
                if each['data'].name == "Function" and each["data"].keyword == name_of_function.value:
                    return each

        if not data and self.parser:
            print(self.parser.program())
            ast = self.parser.root_ast
        else:
            ast = data
        #print(ast)
        if ast:
            for node in ast:
                #f"{node.keyword.value}_{str(uuid.uuid4())[:8]}"
                self.context[node.keyword.value] = { "type": node , "data": node.value}
                if node.name == "CallingFunction":
                    fn = search_function(node.keyword)
                    print(fn["data"].value(node.value))
                elif data:
                    print(f"{node.keyword.value} = {node.value.name}")
            #print(self.context)

if __name__ == '__main__':
    Interpret(True).interpret()
