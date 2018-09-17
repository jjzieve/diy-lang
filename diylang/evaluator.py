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

operators = ['+', '-', '/', '*', 'mod', '>']
def equal(x, y):
    if not is_atom(x) or not is_atom(y):
        return False
    return x == y

def arithmetic(x, y, op):
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
    raise DiyLangError('Operator {0} not supported' % op)

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_list(ast):
        if len(ast) == 0:
            return ast
        first, rest = ast[0], ast[1:]
        if first == 'quote':
            return rest[0]
        if first == 'atom':
            return is_atom(evaluate(rest, env))
        if first == 'eq': # assumes 2 args to arithmetic and eq operators
            x = evaluate(rest[0], env)
            y = evaluate(rest[1], env)
            return equal(x, y)
        if first in operators:
            x = evaluate(rest[0], env)
            y = evaluate(rest[1], env)
            return arithmetic(x, y, first)
        if first == '-':
            return evaluate(ast[1], env) - evaluate(ast[2], env)
        return evaluate(first, env)
    else:
        return ast


