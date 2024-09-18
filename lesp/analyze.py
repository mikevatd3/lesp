from .datatypes import Symbol, Atom, Exp, List
from .core import STANDARD_ENV, parse


def inner_extract(program: Exp, result: set, env):
    for item in program:
        match item:
            case List():
                inner_extract(item, result, env)
            case Symbol():
                if item not in env:
                    result.add(item)
            case _:
                pass


def extract_variables(lesp_code: str, env=STANDARD_ENV) -> set[str]:
    """
    This will get more complicated when we're introducing new data
    sources that we want to include as vars in these strings.
    """

    result = set()

    program = parse(lesp_code)

    # If program is only one token return it wrapped in a set
    if type(program) != list:
        if program not in env:
            return {program}

    inner_extract(parse(lesp_code), result, env)

    return result


class LespCompileError(Exception):
    """
    This is returned from the lesp validation function. The message
    provides more specifics. TODO I'd like to provide the user with
    exactly where the item is breaking down.
    """


def validate_program(program: str, env=STANDARD_ENV):
    """
    This is the validate that starts at the string-representation of the
    program. It responds correctly to parse errors.
    """
    try:
        expression = parse(program)
        return validate_expression(expression, env=env)

    except (SyntaxError, IndexError) as e:
        match e:
            case SyntaxError():
                raise LespCompileError("unexpected )")
            case IndexError():
                raise LespCompileError("( was not closed")


def validate_expression(program: Exp | Atom, env=STANDARD_ENV):
    if isinstance(program, Atom):
        if program in env:
            raise LespCompileError("Invalid lesp code.")
        return

    stack = []
    stack.append(program)
    while stack:
        program = stack.pop()
        match program:
            case [Symbol(op), *args]:
                if op not in env:
                    raise LespCompileError(
                        "Every ( ) expression must start with an operation: + - / *."
                    )
                stack.extend(args)
            case Symbol(op):
                if op in env:
                    raise LespCompileError(
                        "Operations, + - / *, can only be placed at the beginning of the ( ) expression."
                    )
            case _:
                continue
