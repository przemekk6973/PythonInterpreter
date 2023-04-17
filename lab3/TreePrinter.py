from __future__ import print_function
import AST as AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, tabs):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.BinaryExpr)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print(self.op)
        self.left.printTree(tabs + 1)
        self.right.printTree(tabs + 1)

    @addToClass(AST.AssignOperation)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print(self.op)
        self.left.printTree(tabs + 1)
        self.right.printTree(tabs + 1)

    @addToClass(AST.IfCondition)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print("IF")
        self.cond.printTree(tabs + 1)
        self.if_body.printTree(tabs + 1)
        if self.else_body is not None:
            self.print_tab(tabs)
            print("ELSE")
            self.else_body.printTree(tabs + 1)

    @addToClass(AST.While)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print("WHILE")
        self.cond.printTree(tabs + 1)
        self.body.printTree(tabs + 1)

    @addToClass(AST.For)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print("FOR")
        self.begin.printTree(tabs + 1)
        self.end.printTree(tabs + 1)
        self.body.printTree(tabs + 1)

    @addToClass(AST.Break)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print("BREAK")

    @addToClass(AST.Continue)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print("CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print("RETURN")
        if self.expr is not None:
            self.expr.printTree(tabs + 1)

    @addToClass(AST.Print)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print("PRINT")
        for expr in self.exprs:
            expr.printTree(tabs + 1)

    @addToClass(AST.Transpose)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print("TRANSPOSE")
        self.arg.printTree(tabs + 1)

    @addToClass(AST.Function)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print(self.function)
        self.arg.printTree(tabs + 1)

    @addToClass(AST.Matrix)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print("VECTOR")
        for row in self.matrix:
            self.print_tab(tabs + 1)
            print("VECTOR")
            for expr in row:
                self.print_tab(tabs + 2)
                print(expr)

    @addToClass(AST.Uminus)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print("-")
        self.arg.printTree(tabs + 1)

    @addToClass(AST.ID)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print(self.id)

    @addToClass(AST.Assignable)
    def printTree(self, tabs):
        self.id.printTree(tabs)
        if self.index is not None:
            self.print_tab(tabs)
            print("REF")
            for expr in self.index:
                self.print_tab(tabs + 1)
                print(expr)

    @addToClass(AST.String)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print("STRING")
        self.print_tab(tabs + 1)
        print(self.string)

    @addToClass(AST.Instructions)
    def printTree(self, tabs):
        for instruction in self.instructions:
            instruction.printTree(tabs)

    @addToClass(AST.IntNum)
    def printTree(self, tabs):
        self.print_tab(tabs)
        print(self.value)

    @addToClass(AST.Float)
    def printTree(self, tabs=0):
        self.print_tab(tabs)
        print(self.value)

    @addToClass(AST.Instructions)
    def printTree(self, tabs):
        for instruction in self.instructions:
            instruction.printTree(0)

    @addToClass(AST.Error)
    def printTree(self, tabs=0):
        pass
