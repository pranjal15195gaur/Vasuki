from dataclasses import dataclass
import builtins

class AST:
    pass

# New Environment class for static scoping
class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}
    def lookup(self, name):
        if name in self.values:
            return self.values[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise ValueError(f"Variable {name} not defined")
    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
        elif self.parent is not None:
            self.parent.assign(name, value)
        else:
            raise ValueError(f"Variable {name} not defined")
    def declare(self, name, value):
        self.values[name] = value

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class UnOp(AST):
    op: str
    num: AST

@dataclass
class Float(AST):
    val: str

@dataclass
class Int(AST):
    val: str

@dataclass
class Parentheses(AST):
    val: AST

@dataclass
class If(AST):
    cond: AST
    then: AST
    elseif_branches: list[tuple[AST, AST]]
    elsee: AST

@dataclass
class VarDecl(AST):
    name: str
    value: AST

@dataclass
class VarReference(AST):
    name: str

@dataclass
class Assignment(AST):
    name: str
    value: AST

@dataclass
class Program(AST):
    statements: list[AST]

@dataclass
class For(AST):
    init: AST
    condition: AST
    increment: AST
    body: AST

@dataclass
class While(AST):
    condition: AST
    body: AST

@dataclass
class Print(AST):
    expr: AST

@dataclass
class FunctionCall(AST):
    name: str
    args: list[AST]

@dataclass
class Label(AST):
    name: str

@dataclass
class LabelReturn(AST):
    name: str

@dataclass
class GoAndReturn(AST):
    name: str

def e(tree: AST, env=None) -> int:
    if env is None:
        env = Environment()

    match tree:
        case Program(stmts):
            result = None
            # Evaluate statements in the global environment
            for stmt in stmts:
                result = e(stmt, env)
            return result

        case VarDecl(name, value):
            result = e(value, env)
            env.declare(name, result)
            return result

        case Assignment(name, value):
            result = e(value, env)
            env.assign(name, result)
            return result

        case VarReference(name): 
            return env.lookup(name)
        case Int(v): 
            return int(v)
        case Float(v): 
            return float(v)
        case UnOp("-", expp): 
            return -1 * e(expp, env)

        case BinOp(op, l, r):
            left_val = e(l, env)
            right_val = e(r, env)
            match op:
                case "**": return left_val ** right_val
                case "*": return left_val * right_val
                case "/":
                    if isinstance(left_val, int) and left_val%(right_val)==0 :
                        return left_val // right_val
                    return left_val / right_val
                case "%": return left_val % right_val       # support for modulo operator
                case "+": return left_val + right_val
                case "-": return left_val - right_val
                case "<": return left_val < right_val
                case "<=": return left_val <= right_val
                case ">": return left_val > right_val
                case ">=": return left_val >= right_val
                case "==": return left_val == right_val
                case "!=": return left_val != right_val
                case "and": return (left_val and right_val)    # logical and
                case "or": return (left_val or right_val)      # logical or
                case _: raise ValueError(f"Unsupported binary operator: {op}")

        case Parentheses(expp): 
            return e(expp, env)

        case If(cond, then, elseif_branches, elsee):
            if cond is None:
                raise ValueError("Condition missing in 'if' statement")
            for elseif_cond, _ in elseif_branches:
                if elseif_cond is None:
                    raise ValueError("Condition missing in 'elseif' statement")
            if e(cond, env):
                # Create a new static (child) environment for the then block
                return e(then, Environment(env))
            for elseif_cond, elseif_then in elseif_branches:
                if e(elseif_cond, env):
                    # New child environment for elseif block
                    return e(elseif_then, Environment(env))
            if elsee is not None:
                # New child environment for else block
                return e(elsee, Environment(env))
            return None

        case For(init, condition, increment, body):
            # Evaluate initialization in current env
            e(init, env)
            result = None
            # Loop while condition is true
            while e(condition, env):
                # Execute body in a new child environment for static scoping
                result = e(body, Environment(env))
                # Execute increment in current env
                e(increment, env)
            return result

        case While(condition, body):
            result = None
            while e(condition, env):
                result = e(body, env)
            return result

        case Print(expr):
            value = e(expr, env)
            print(value)
            return value

        case FunctionCall(name, args):
            evaluated_args = [e(a, env) for a in args]
            if name == "max":
                return max(*evaluated_args)
            elif name == "min":
                return min(*evaluated_args)
            else:
                raise ValueError(f"Unknown function {name}")

        case Label(name):
            # Just a marker, do nothing
            return None
        case LabelReturn(name):
            # Also just a marker, do nothing
            return None
        case GoAndReturn(name):
            # Interpret the labeled block again, reusing same env
            labeled_ast = find_label_block(name)
            if not labeled_ast:
                raise ValueError(f"Label {name} not found")
            return run_label_block(labeled_ast, name, env)

        case _:
            raise ValueError("Unsupported node type")


def find_label_block(label_name: str):
    """
    Searches the global program statements for a matching label.
    Collects statements until a matching LabelReturn is found.
    Returns the collected statements or None if not found.
    """
    global_program = getattr(builtins, 'global_program', None)
    if not global_program or not isinstance(global_program, Program):
        return None

    in_block = False
    block_stmts = []
    for stmt in global_program.statements:
        if isinstance(stmt, Label) and stmt.name == label_name:
            in_block = True
            continue
        if in_block:
            if isinstance(stmt, LabelReturn) and stmt.name == label_name:
                return block_stmts
            block_stmts.append(stmt)
    return None

def run_label_block(stmts, label_name, env):
    """
    Executes the statements collected by find_label_block
    until a LabelReturn with the same name or the end.
    """
    if not stmts:
        return None

    for stmt in stmts:
        if isinstance(stmt, LabelReturn) and stmt.name == label_name:
            return None
        e(stmt, env)
    return None