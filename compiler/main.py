from compiler.parser import parse
from compiler.top import e
import sys

code = sys.argv[1]

code = open(code).read()


ast = parse(code)
e(ast)

