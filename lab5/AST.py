class Node(object):
    def print_tab(self, indent):
        print("|   " * indent, end="")


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinaryExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssignOperation(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class IfCondition(Node):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class While(Node):
    def __init__(self, condition, body):
        self.body = body
        self.condition = condition


class For(Node):
    def __init__(self, var, begin, end, body):
        self.var = var
        self.begin = begin
        self.end = end
        self.body = body


class Break(Node):
    def __init__(self):
        pass


class Continue(Node):
    def __init__(self):
        pass


class Return(Node):
    def __init__(self, expr=None):
        self.expr = expr


class Print(Node):
    def __init__(self, exprs):
        self.exprs = exprs


class Transpose(Node):
    def __init__(self, arg):
        self.arg = arg


class Uminus(Node):
    def __init__(self, arg):
        self.arg = arg


class Function(Node):
    def __init__(self, function, argument):
        self.function = function
        self.arg = argument


class Matrix(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class ID(Node):
    def __init__(self, id):
        self.id = id


class Assignable(Node):
    def __init__(self, id, index=None):
        self.id = id
        self.index = index


class String(Node):
    def __init__(self, string):
        self.string = string


class Instructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Float(Node):
    def __init__(self, value):
        self.value = value


class Start(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Printable(Node):
    def __init__(self, printables):
        self.printables = printables



class Error(Node):
    def __init__(self):
        pass