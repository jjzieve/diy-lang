# -*- coding: utf-8 -*-

from .types import Environment, DiyLangError, Closure, String
from .ast import is_boolean, is_atom, is_symbol, is_list, is_closure, \
    is_integer, is_string
from .parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports,
making your work a bit easier. (We're supposed to get through this thing
in a day, after all.)
"""

# Helper evaluaters
def evaluate_equal(rest, env):
    # assumes 2 args
    x = evaluate(rest[0], env)
    y = evaluate(rest[1], env)
    if not is_atom(x) or not is_atom(y):
        return False
    return x == y

def evaluate_arithmetic(first, rest, env):
    operator = first
    # assumes 2 args x, y
    x = evaluate(rest[0], env)
    y = evaluate(rest[1], env)
    if not is_integer(x) or not is_integer(y):
        raise DiyLangError('One or more inputs are not Integers')
    if operator == '+':
        return x + y
    if operator == '-':
        return x - y
    if operator == '*':
        return x * y
    if operator == '/':
        return x // y
    if operator == 'mod':
        return x % y
    if operator == '>':
        return x > y
    raise DiyLangError('Operator {0} not supported'.format(operator))

def evaluate_define(rest, env):
    if len(rest) != 2:
        raise DiyLangError('Wrong number of arguments')
    variable = rest[0]
    value = evaluate(rest[1], env)
    if not is_symbol(variable):
        raise DiyLangError('{0} is not a symbol')
    env.set(variable, value)
    return variable

def evaluate_if(rest, env):
    if evaluate(rest[0], env): # predicate
        return evaluate(rest[1], env) # arg1
    return evaluate(rest[2], env) # arg2

def evaluate_quote(rest):
    return rest[0]

def evaluate_atom(rest, env):
    return is_atom(evaluate(rest[0], env))

def call(closure, args, env):
    if len(args) != len(closure.params):
        raise DiyLangError("wrong number of arguments, expected {0} got {1}".format(len(closure.params), len(args)))
    evaluated_args = [evaluate(arg, env) for arg in args]
    new_env = closure.env.extend(dict(zip(closure.params, evaluated_args)))
    return evaluate(closure.body, new_env)

def evaluate_lambda(rest, env):
    if len(rest) != 2:
        raise DiyLangError('incorrect number of arguments')
    if not is_list(rest[0]):
        raise DiyLangError('lambda parameters must be a list')
    params = rest[0]
    body = rest[1]
    return Closure(env, params, body)

def evaluate_cons(rest, env):
    _list = evaluate(rest[1], env)
    new_element = evaluate(rest[0], env)
    return [new_element] + _list

def evaluate_cond(rest, env):
    for tup in rest[0]:
        if evaluate(tup[0], env):
            return evaluate(tup[1], env)
    return False

def evaluate_head(rest, env):
    _list = evaluate(rest[0], env)
    if is_list(_list) and len(_list) != 0:
        return _list[0]
    raise DiyLangError("Failed to call head on non-list or empty list")

def evaluate_tail(rest, env):
    _list = evaluate(rest[0], env)
    if is_list(_list) and len(_list) != 0:
        return _list[1:]
    raise DiyLangError("Failed to call tail on non-list or empty list")

def evaluate_empty(rest, env):
    _list = evaluate(rest[0], env)
    if is_list(_list):
        if len(_list) == 0:
            return True
        return False
    raise DiyLangError("Failed to call empty on non-list")

def evaluate_list(ast, env):
    if len(ast) == 0:
        raise DiyLangError("Failed to evaluate empty list")
    # Check if first is a form/keyword then do some logic on the rest
    first, rest = ast[0], ast[1:]
    if first == 'lambda':
        return evaluate_lambda(rest, env)
    elif first == 'cons': # cons'truct a list
        return evaluate_cons(rest, env)
    elif first == 'head':
        return evaluate_head(rest, env)
    elif first == 'tail':
        return evaluate_tail(rest, env)
    elif first == 'empty':
        return evaluate_empty(rest, env)
    elif first == 'define':
        return evaluate_define(rest, env)
    elif first == 'quote':
        return evaluate_quote(rest)
    elif first == 'atom':
        return evaluate_atom(rest, env)
    elif first == 'if':
        return evaluate_if(rest, env)
    elif first == 'cond':
        return evaluate_cond(rest, env)
    elif first == 'eq':
        return evaluate_equal(rest, env)
    elif first in ['+', '-', '/', '*', 'mod', '>']:
        return evaluate_arithmetic(first, rest, env)
    elif is_closure(first): # Call the closure/function
        return call(first, rest, env)
    elif is_symbol(first) or is_list(first): # if variable or another list, attempt to evaluate and call immediately
        return evaluate([evaluate(first, env)] + rest, env)
    else:
        raise DiyLangError("{0} is not a function".format(first))

# Main evaluator
def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_symbol(ast):
        return env.lookup(ast)
    elif is_list(ast):
        return evaluate_list(ast, env)
    return ast
