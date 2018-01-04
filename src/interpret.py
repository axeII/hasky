"""Parser

Syntactic analyzator for discovering grammar

"""
__author__ = 'ales lerch'

#import uuid
import types
from parser import Parser
from lexer import Token
from ast import Function, List
from latex import Latex
from util import FunctionNotFound, ContextValue, untoken, ast_value, DiffenrentTypes

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
        print("""
.__                   __           
|  |__ _____    _____|  | _____.__.
|  |  \\__   \\  /  ___/  |/ <   |  | | hasky alpha v. 0.0.4
|   Y  \/ __ \_\___ \|    < \___  | | demo version
|___|  (____  /____  >__|_ \/ ____| | 
     \/     \/     \/     \/\/     
""")
        while True:
            try:
                text_ = input('hasky> ')
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
                    "+", None, lambda x, y: self.control_values(x, y) + self.control_values(y, x)
                )
            ),
            "-": ContextValue(
                "default", Function(
                    "-", None, lambda x, y: self.control_values(x, y) - self.control_values(y, x)
                )
            ),
            "/": ContextValue(
                "default", Function(
                    "/", None, lambda x, y: self.control_values(x, y) * self.control_values(y, x)
                )
            ),
            "*": ContextValue(
                "default", Function(
                    "*", None, lambda x, y: self.control_values(x, y) / self.control_values(y, x)
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
            "latex": ContextValue(
                "default", Function(
                    "latex", None, lambda a: Latex(untoken(ast_value(a))).outprint()
                )
            ),
        }

    def print_context_data(self):
        for key, val in self.context.items():
            print(f" {key}: {val.cont_val_data.value}")

    def control_values(self, a, b):

        def unbox(value_):
            try:
                return untoken(ast_value(value_.cont_val_data))
            except:
                return untoken(ast_value(value_))

        if type(unbox(a)) == type(unbox(b)):
            return unbox(a)
        elif unbox(a) in self.context:
            return unbox(self.context[unbox(a)])
        elif unbox(b) in self.context:
            return unbox(a)
        else:
            raise DiffenrentTypes("You are trying to call fucntion on two different types")

    def interpret(self, data=None, ast=[]):

        def return_lambda(fn, args, contx):
                if fn in contx:
                    if contx[fn].cont_val_type == "default":
                        return ast_value(contx[fn].cont_val_data)(*args)
                    else:
                        """this feauture shoudl be added to control_values fucntion"""
                        data = list(map(lambda x: untoken(x.value), ast_value(contx[fn].cont_val_data)))
                        lambda_ = eval(f"lambda {data[1]}: {data[1]} {data[0]} {data[2]}")
                        return lambda_(*args)
                else:
                    return fn

        def search_function(name_of_function):
            for searching_fn in list(filter(lambda x: x.cont_val_type != "CallingFunction", self.context.values())):
                if searching_fn.cont_val_data.name == "Function" and\
                   untoken(searching_fn.cont_val_data.keyword) == name_of_function.token_value:
                    return searching_fn

            raise FunctionNotFound(f"Function {untoken(name_of_function)} not found")

        def check_context(local_cont, glob_cont, ch_val):
            try:
                found = local_cont[ch_val]
                """ if foudn fn is in global need to continue"""
                return found
            except KeyError:
                if ch_val in glob_cont:
                    return glob_cont[ch_val].cont_val_data.value
                else:
                    print(f"{ch_val} not found")
                """elif local_cont[ch_val] in glob_cont:
                    if glob_cont[local_cont[ch_val]].cont_val_type == "default":
                        return ast_value(glob_cont[local_cont[ch_val]].cont_val_data)
                    else:
                        data = list(map(lambda x: x.cont_val_data,glob_cont[found].cont_val_data.value))
                        return_lambda(data[0], *data[1:], glob_cont)"""

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
            func_ = check_context(set_args, context, untoken(ast_value(fnd_func.cont_val_data.value[0])))
            args_ = list(map(lambda a: ctrlvar_scp(set_args, context, a), fnd_func.cont_val_data.value[1:]))
            if isinstance(func_, types.LambdaType):
                return func_(*args_)
            else:
                return return_lambda(func_, args_, self.context)

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
                    """ if found function is not default user made it"""
                    print(control_eval(found_fn, self.context))
                else:
                    """ fucntion is defautl"""
                    if isinstance(operation.value[0], List):
                        """refactoring need fix dry"""
                        data = list(map(lambda x: untoken(x.value), operation.value[0].value))
                        lambda_ = eval(f"lambda _: {data[1]} {data[0]} {data[2]}")
                        return found_fn.cont_val_data.value(lambda_(None))
                    else:
                        #print(found_fn.cont_val_data.value(*operation.value[0]))
                        try:
                            print(found_fn.cont_val_data.value(*operation.value))
                        except KeyError as e:
                            print(f"Variable {e.args[0]} doesn't exit")
            else:
                self.context[key] = ContextValue(operation.name, operation.value)
                print(f"{operation.keyword.token_value} = {operation.value[0].name}")

if __name__ == '__main__':
    Interpret(None, True).interpret()
