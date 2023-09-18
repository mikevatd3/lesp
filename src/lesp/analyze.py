from .datatypes import Symbol, Number, Atom, Exp, List
from .core import standard_env, parse


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


def validate(lesp_code: str) -> bool:
    """
    TODO: Parse lesp code and make sure it is valid.
    """
    return False


def extract_variables(lesp_code: str, env=standard_env()) -> set[str]:
    """
    This will get more complicated when we're introducing new data
    sources that we want to include as vars in these strings.
    """

    result = set()

    program = parse(lesp_code)
    
    # If program is only one token return it wrapped in a set
    if (type(program) != list):
        if (program not in env):
            return {program}

    inner_extract(parse(lesp_code), result, env)

    return result

