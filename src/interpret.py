"""Parser

Syntactic analyzator for discovering grammar

"""
__author__ = 'ales lerch'

#import uuid
import types
from parser import Parser
from lexer import Token
from ast import Function
from util import FunctionNotFound, ContextValue, untoken, ast_value

class Interpret:

    def __init__(self, inp_file, on_interpreter=False):
        self.token = Token()
        self.parser = None
        #self.context = {}
        self.init_context()
        if on_interpreter:
            self.start_interpreter()
        else:
            self.parser = Parser(self.token.lexer(input_file=inp_file))

    def start_interpreter(self):
        while True:
            try:
                text_ = input('flang> ')
            except EOFError:
                break
            if not text_:
                continue
            parser = Parser(self.token.lexer(text=text_))
            parser.program()
            self.interpret(parser.root_ast)

    def init_context(self):
        self.context = default_functions = {
            "eval": ContextValue(
                "default", Function(
                    "eval", None, lambda x: self.context[x.value.token_value].eval_cvalue()
                )
            ),
            "+": ContextValue(
                "default", Function(
                    "+", None, lambda x, y: untoken(ast_value(x)) + untoken(ast_value(y))
                )
            ),
            "-": ContextValue(
                "default", Function(
                    "-", None, lambda x, y: untoken(ast_value(x)) - untoken(ast_value(y))
                )
            ),
            "/": ContextValue(
                "default", Function(
                    "/", None, lambda x, y: untoken(ast_value(x)) / untoken(ast_value(y))
                )
            ),
            "*": ContextValue(
                "default", Function(
                    "*", None, lambda x, y: untoken(ast_value(x)) * untoken(ast_value(y))
                )
            ),
            "stack": ContextValue(
                "default", Function(
                    "stack", None, lambda _: self.print_context_data()
                )
            ),
            "type": ContextValue(
                "default", Function(
                    "type", None, lambda a: self.context[untoken(ast_value(a))].cont_val_data.name
                )
            ),
        }

    def print_context_data(self):
        for key, val in self.context.items():
            print(f" {key}: {val.cont_val_data.value}")

    def interpret(self, data=None, ast=[]):

        def search_function(name_of_function):
            for searching_fn in list(filter(lambda x: x.cont_val_type != "CallingFunction", self.context.values())):
                if searching_fn.cont_val_data.name == "Function" and\
                   untoken(searching_fn.cont_val_data.keyword) == name_of_function.token_value:
                    return searching_fn

            raise FunctionNotFound(f"Function {untoken(name_of_function)} not found")

        def check_context(local_cont, glob_cont, ch_val):
            #print(ch_val)
            try:
                found = local_cont[ch_val]
                if found in glob_cont:
                    #print('oh',control_eval(glob_cont[found], glob_cont, local_cont))
                    #print('kek:',glob_cont[found].cont_val_data.value)
                    return glob_cont[found].cont_val_data.value
                #print(found)
                return found
            except KeyError:
                if ch_val in glob_cont:
                    return glob_cont[ch_val].cont_val_data.value
                else:
                    print(f"{ch_val} not found")

        def control_eval(fnd_func, context, set_args={}):

            def ctrlvar_scp(local_scope, global_scope, variable):
                """fucntion that controlos value for first local scope
                and then for global scope"""
                if untoken(variable.value) in local_scope:
                    return local_scope[untoken(variable.value)]
                elif untoken(variable.value) in global_scope:
                    return untoken(ast_value(global_scope[untoken(variable.value)].cont_val_data))
                else:
                    return untoken(variable.value)

            for arg_number in range(len(fnd_func.cont_val_data.args)):
                set_args[untoken(fnd_func.cont_val_data.args[arg_number])] =\
                    untoken(operation.value[arg_number].value)

            func_ = check_context(set_args, context, untoken(fnd_func.cont_val_data.value[0].value))
            args_ = list(map(lambda a: ctrlvar_scp(set_args, context, a), fnd_func.cont_val_data.value[1:]))
            print(func_)
            if isinstance(func_, types.LambdaType):
#c = fn f x: f x; pluspet = fn x: + x 5; c pluspet 6;
                return func_(*args_)
            else:
                return func_

        if not data and self.parser:
            print(self.parser.program())
            ast = self.parser.root_ast
        else:
            ast = data if data else []

        for operation in ast:
            #f"{operation.keyword.value}_{str(uuid.uuid4())[:8]}"
            key = untoken(operation.keyword)
            if key in self.context and operation.name != "CallingFunction":
                print(f"Variable {key} already exits")
            elif operation.name == "CallingFunction":
                try:
                    found_fn = search_function(operation.keyword)
                except FunctionNotFound as fnf:
                    print(fnf)
                    return 1
                if found_fn.cont_val_type != "default":
                    """ if found function is defautl"""
                    print(control_eval(found_fn, self.context))
                else:
                    """ if found function is not defautl e.g. user made it"""
                    #print(operation, *operation.value)
                    print(found_fn.cont_val_data.value(*operation.value))
            else:
                self.context[key] = ContextValue(operation.name, operation.value)
                print(f"{operation.keyword.token_value} = {operation.value[0].name}")
        #self.print_context_data()

if __name__ == '__main__':
    Interpret(None, True).interpret()
