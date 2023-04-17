import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

binOps = {
    "+": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "/": (lambda x, y: x / y),
    ">": (lambda x, y: x > y),
    "<": (lambda x, y: x < y),
    ">=": (lambda x, y: x >= y),
    "<=": (lambda x, y: x <= y),
    "==": (lambda x, y: x == y),
    "!=": (lambda x, y: x != y),
}

binOpsMatrix = {
    ".+": (lambda x, y: x + y),
    ".-": (lambda x, y: x - y),
    ".*": (lambda x, y: x * y),
    "./": (lambda x, y: x / y),
    "+": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "*": (lambda x, y: np.dot(x, y)),
    "/": (lambda x, y: np.linalg.solve(y, x)),
}

assignOps = {
    "=": (lambda _, y: y),
    "+=": binOps["+"],
    "-=": binOps["-"],
    "*=": binOps["*"],
    "/*": binOps["/"],
}

assignOpsMatrix = {
    "+=": binOpsMatrix["+"],
    "-=": binOpsMatrix["-"],
    "*=": binOpsMatrix["*"],
    "/=": binOpsMatrix["/"],
}


class Interpreter(object):
    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Num)
    def visit(self, node):
        if isinstance(node.value, int):
            return int(node.value)
        else:
            return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException

    @when(AST.Return)
    def visit(self, node):
        return node.val.accept(self)

    @when(AST.Error)
    def visit(self, node):
        pass

    @when(AST.Cond)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.rel_op
        return binOps[op](r1, r2)

    @when(AST.Vector)
    def visit(self, node):
        return np.array([elem.accept(self) for elem in node.vector])

    @when(AST.Matrix)
    def visit(self, node):
        return np.array([vector.accept(self) for vector in node.matrix])

    @when(AST.MatrixFunction)
    def visit(self, node):
        if node.func == "eye":
            return np.eye(node.value)
        elif node.func == "ones":
            return np.ones(node.value)
        else:
            return np.zeros((node.value, node.value))

    @when(AST.Transposition)
    def visit(self, node):
        matrix = node.matrix.accept(self)
        return np.transpose(matrix)

    @when(AST.If)
    def visit(self, node):
        if node.condition.accept(self):
            self.memoryStack.push(Memory("if"))
            r = node.instruction.accept(self)
            self.memoryStack.pop()
            return r

    @when(AST.IfElse)
    def visit(self, node):
        if node.condition.accept(self):
            self.mamoryStack.push(Memory("if"))
            r = node.instruction.accept(self)
            self.memoryStack.pop()
            return r
        else:
            self.memoryStack.push(Memory("else"))
            r = node.else_instruction.accept(self)
            self.memoryStack.pop()
            return r

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.bin_op
        if self.is_multidimentional(r1) or self.is_multidimentional(r2) and op in binOpsMatrix:
            return binOpsMatrix[op](r1, r2)
        else:
            return binOps[op](r1, r2)

    def is_num(self, val):
        return isinstance(val, int) or isinstance(val, float)

    def is_string(self, val):
        return isinstance(val, str)

    @when(AST.AssignOperation)
    def visit(self, node):
        var = node.variable
        expression_val = node.expression.accept(self)
        op = node.op

        if isinstance(var, AST.MatrixElement):
            id, x, y = var.id.id, var.index_x, var.index_y
            matrix = self.memoryStack.get(id)
            matrix[x][y] = assignOps[op](matrix[x][y], expression_val)
        elif isinstance(var, AST.VectorElement):
            vector_id, x = var.id, var.index
            vector = self.memoryStack.get(vector_id)
            vector[x] = assignOps[op](vector[x], expression_val)
        else:
            if op == "=":
                if self.memoryStack.get(var.id) is not None:
                    self.memoryStack.set(var.id, expression_val)
                else:
                    self.memoryStack.insert(var.id, expression_val)
            else:
                curr_value = self.memoryStack.get(var.id)
                new_value = assignOps[op](curr_value, expression_val) \
                    if self.is_multidimentional(expression_val) \
                    else assignOps[op](curr_value, expression_val)
                self.memoryStack.set(var.id, new_value)



    def is_multidimentional(self, obj):
        return isinstance(obj, np.ndarray)

    def check_matrix_and_value_type(self, matrix_elem, value):
        return type(matrix_elem) == type(value)  # zakładamy, że w macierzy znajdują się dobre wartości

    @when(AST.ID)
    def visit(self, node):
        var_name = node.id
        return self.memoryStack.get(var_name)

    @when(AST.VectorElement)
    def visit(self, node):
        vector = node.id.accept(self)
        index = node.index.accept(self)
        return vector[index]

    @when(AST.MatrixElement)
    def visit(self, node):
        matrix = node.id.accept(self)
        return matrix[node.index_x, node.index_y]


    @when(AST.WhileLoop)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                self.memoryStack.push(Memory("while"))
                node.instruction.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break
            finally:
                self.memoryStack.pop()


    @when(AST.ForLoop)
    def visit(self, node):
        loop_range = node.f_range.accept(self)
        if self.memoryStack.get(node.l_id.id):
            self.memoryStack.set(node.l_id.id, loop_range.start)
        else:
            self.memoryStack.insert(node.l_id.id, loop_range.start)

        while self.memoryStack.get(node.l_id.id) <= (len(loop_range) + loop_range.start - 1):
            try:
                self.memoryStack.push(Memory("for"))
                node.instruction.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            finally:
                self.memoryStack.pop()

            new = self.memoryStack.get(node.l_id.id) + 1
            self.memoryStack.set(node.l_id.id, new)

    @when(AST.Range)
    def visit(self, node):
        start, stop = node.start.accept(self), node.end.accept(self)
        return range(start, stop + 1)

    @when(AST.Print)
    def visit(self, node):
        print(node.print_vars.accept(self))

    @when(AST.PrintVals)
    def visit(self, node):
        return " ".join([str(print_val.accept(self)) for print_val in node.vals])