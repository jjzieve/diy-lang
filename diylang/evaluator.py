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

def equal(rest, env):
    # assumes 2 args
    x = evaluate(rest[0], env)
    y = evaluate(rest[1], env)
    if not is_atom(x) or not is_atom(y):
        return False
    return x == y

def arithmetic(first, rest, env):
    op = first
    # assumes 2 args x, y
    x = evaluate(rest[0], env)
    y = evaluate(rest[1], env)
    if not is_integer(x) or not is_integer(y):
        raise DiyLangError('One or more inputs are not Integers')
    if op == '+':
        return x + y
    if op == '-':
        return x - y
    if op == '*':
        return x * y
    if op == '/':
        return x // y
    if op == 'mod':
        return x % y
    if op == '>':
        return x > y
    raise DiyLangError('Operator {0} not supported'.format(op))

def define(rest, env):
    if len(rest) != 2:
        raise DiyLangError('Wrong number of arguments')
    variable = rest[0]
    value = evaluate(rest[1], env)
    if not is_symbol(variable):
        raise DiyLangError('{0} is not a symbol')
    env.set(variable, value)
    return variable

def control(rest, env):
    if evaluate(rest[0], env): # predicate
        return evaluate(rest[1], env) # arg1
    return evaluate(rest[2], env) # arg2

def quote(rest):
    return rest[0]

def atom(rest, env):
    return is_atom(evaluate(rest[0], env))

def call_closure(closure, args, env):
    if len(args) != len(closure.params):
        raise DiyLangError("wrong number of arguments, expected {0} got {1}".format(len(closure.params), len(args)))
    evaluated_args = [evaluate(arg, env) for arg in args]
    new_env = closure.env.extend(dict(zip(closure.params, evaluated_args)))
    return evaluate(closure.body, new_env)

def create_closure(rest, env):
    if len(rest) != 2:
        raise DiyLangError('incorrect number of arguments')
    if not is_list(rest[0]):
        raise DiyLangError('lambda parameters must be a list')
    params = rest[0]
    body = rest[1]
    return Closure(env, params, body)
    
operators = ['+', '-', '/', '*', 'mod', '>']
def evaluate_list(ast, env):
    if len(ast) == 0:
        raise DiyLangError("failed to evaluate empty list")

    first, rest = ast[0], ast[1:]
    if first == 'lambda':
        return create_closure(rest, env)
    elif first == 'define':
        return define(rest, env)
    elif first == 'quote':
        return quote(rest)
    elif first == 'atom':
        return atom(rest, env)
    elif first == 'if':
        return control(rest, env)
    elif first == 'eq':
        return equal(rest, env)
    elif first in operators:
        return arithmetic(first, rest, env)
    elif is_closure(first):
        return call_closure(first, rest, env)
    elif is_symbol(first) or is_list(first): # if variable or list (e.g. lambda), attempt to call/evaluate immediately
        return evaluate([evaluate(first, env)] + rest, env)
    else:
        raise DiyLangError("{0} is not a function".format(first))
            
def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_symbol(ast):
        return env.lookup(ast)
    elif is_list(ast):
        return evaluate_list(ast, env)
    return ast
