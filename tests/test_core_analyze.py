from lesp.core import read_from_tokens, tokenize, atom, execute, parse
from lesp.datatypes import Symbol, Number
from lesp.analyze import extract_variables, validate_program, LespCompileError


def test_tokenize():
    result = tokenize("(* 100 (/ (+ B09019012 B09019013) B09019001))")

    assert result == [
        "(",
        "*",
        "100",
        "(",
        "/",
        "(",
        "+",
        "B09019012",
        "B09019013",
        ")",
        "B09019001",
        ")",
        ")",
    ]


def test_atom():
    assert type(atom("*")) == Symbol
    assert type(atom("2")) == Number


def test_read_from_tokens():
    program = [
        "(",
        "*",
        "100",
        "(",
        "/",
        "(",
        "+",
        "B09019012",
        "B09019013",
        ")",
        "B09019001",
        ")",
        ")",
    ]

    expr = read_from_tokens(program)
    assert expr == [
        "*",
        100.0,
        ["/", ["+", "B09019012", "B09019013"], "B09019001"],
    ]


def test_parse():
    assert parse("(* 100 (/ (+ B09019012 B09019013) B09019001))") == [
        "*",
        100.0,
        ["/", ["+", "B09019012", "B09019013"], "B09019001"],
    ]


def test_if():
    assert execute("(if (<= 5 5) 1000 500)", {}) == 1000


def test_extract_variables():
    result = extract_variables("(* 100 (/ (+ B09019012 B09019013) B09019001))")
    
    assert result == {'B09019012', 'B09019013', 'B09019001'}


def test_execute():
    lesp_string = "(* 100 (/ (+ B09019012 B09019013) B09019001))"

    namespace = {
            "B09019012": 1000, 
            "B09019013": 1000,
            "B09019001": 3000,
    }

    assert execute(lesp_string, namespace) == (100 * (2/3))


def test_bad_parse():
    try:
        parse("(+ (+ 100 100)")
    except IndexError:
        return
    assert False

def test_bad_parse_two():
    # This particular example should result in a parse/syntax error
    try:
        result = "+ (+ 100 100)))"
        validate_program(result)
        assert False
    except LespCompileError:
        assert True


def test_validate_one():
    validate_program("(+ 100 100)")


def test_validate_two():
    try:
        validate_program("(+ (+ 100 100 100) (/ 100 100 100)")
        assert False

    except LespCompileError as e:
        assert e.args[0] ==  "( was not closed"


def test_validate_three():
    try:
        program = "(+) (100 + 100) (/ 100 100 100)"
        validate_program(program)

        print(parse(program))

        assert False
    except LespCompileError as e:
        assert e.args[0] ==  "unexpected )"

