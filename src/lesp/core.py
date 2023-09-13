import operator as op
from functools import reduce
from .datatypes import (
    Symbol,
    Number,
    Atom,
    Exp,
    Env,
)


def tokenize(chars: str) -> list[str]:
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def atom(token: str) -> Atom:
    """
    All numbers are floats in this system matching the current implementation.
    """
    try: return float(token)
    except ValueError:
        return Symbol(token)


def read_from_tokens(tokens: list[str]) -> Exp | Atom:
    if len(tokens) == 0:
        raise SyntaxError("Expected EOF")
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("unexpected ')'")
    else:
        return atom(token)


def parse(program: str) -> Exp | Atom:
    return read_from_tokens(tokenize(program))


def standard_env() -> Env:
    """
    An env pared way back from the blog example.
    """

    env = {
        "+": op.add,
        "/": op.truediv,
        "*": op.mul,
        ">": op.gt,
        "<": op.lt,
        "<=": op.le,
        ">=": op.ge,
        "==": op.eq,
    }

    return env


def eval(x: Exp, env, namespace: dict) -> float | bool | Exp:
    match x:
        case Symbol(val):
            if val in env.keys():
                return env[val]
            elif val in namespace:
                return namespace[val]
            raise NameError(f"{val} isn't an operator or in the available namespace")
        case Number(val):
            return x
        case ["if", *args]:
            (_, test, conseq, alt) = x
            exp = (conseq if eval(test, env, namespace) else alt)
            return eval(exp, env, namespace)
        case _:
            proc = eval(x[0], env, namespace)
            args = [eval(arg, env, namespace) for arg in x[1:]]
            return reduce(proc, args)


def execute(expression: str, namespace: dict) -> float | bool:
    "This is a closure over eval with the standard operations env"
    return eval(parse(expression), standard_env(), namespace) 

