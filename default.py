"""Default

Default value for settings value

"""
__author__ = 'ales lerch'


"""    def eval_cvalue(self):
        return self.cv_data._eval()

    def df_plus(val_a, val_b):
        return val_a + val_b

    def df_eval(eval_val, context):
        lambda x: self.context[x.value.token_value].eval_cvalue())
"""

default_functions = {
        "evaluator": ContextValue("default", Function("eval", None, ),
        "pluserer": ContextValue("default", Function("+"), None, df_plus()),
        }

