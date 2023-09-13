from src.lesp.core import read_from_tokens, tokenize, atom, execute, parse
from src.lesp.datatypes import Symbol, Number
from src.lesp.analyze import extract_variables


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


if __name__ == "__main__":
    test_tokenize()
    test_atom()
    test_read_from_tokens()
    test_parse()
    test_if()
    test_extract_variables()
