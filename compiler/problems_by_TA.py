from top import e
from parser import parse, ParseError

def problem_by_TA():
    # Problem statement : Write the multiplication table of 17 till 15 terms
    code = """
            if 2 < 3 { 4 } else if { 5 }
           """

    ast = parse(code)
    e(ast)


if __name__ == "__main__":
    problem_by_TA()