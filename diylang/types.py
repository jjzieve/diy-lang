# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The DiyLangError class you can have for free :)
"""


class DiyLangError(Exception):
    """General DIY Lang error class."""
    pass


class Closure(object):

    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __repr__(self):
        return "<closure/%d>" % len(self.params)


class Environment(object):

    def __init__(self, variables=None):
        self.bindings = variables if variables else {}

    def lookup(self, symbol):
        if symbol not in self.bindings:
            raise DiyLangError('{0} not defined'.format(symbol))
        return self.bindings[symbol]

    def extend(self, variables):
        newVariables = self.bindings.copy()
        newVariables.update(variables)
        return Environment(newVariables)

    def set(self, symbol, value):
        if symbol in self.bindings:
            raise DiyLangError('{0} already defined'.format(symbol))
        self.bindings[symbol] = value;

class String(object):

    """
    Simple data object for representing DIY Lang strings.

    Ignore this until you start working on part 8.
    """

    def __init__(self, val=""):
        self.val = val

    def __str__(self):
        return '"{}"'.format(self.val)

    def __eq__(self, other):
        return isinstance(other, String) and other.val == self.val
