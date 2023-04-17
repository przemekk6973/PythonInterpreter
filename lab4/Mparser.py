import scanner
import ply.yacc as yacc
import AST as AST

tokens = scanner.tokens
precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
    ('nonassoc', '<', '>', 'GEQ', 'LEQ', 'EQ', 'NEQ'),
    ('left', '+', '-'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('left', "'"),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_start(p):
    """start :
            | instructions"""
    p[0] = AST.Instructions(p[1])


def p_instructions(p):
    """ instructions : instruction
                    | instructions instruction"""
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]


def p_break(p):
    """break : BREAK"""
    p[0] = AST.Break()


def p_continue(p):
    """continue : CONTINUE"""
    p[0] = AST.Continue()


def p_instruction(p):
    """ instruction : instruction_if
                | instruction_for
                | instruction_while
                | instruction_return ';'
                | instruction_assign ';'
                | instruction_print ';'
                | break ';'
                | continue ';' """
    p[0] = p[1]


def p_scope(p):
    """ instruction : '{' instructions '}' """
    p[0] = AST.Instructions(p[2])


def p_instruction_return(p):
    """ instruction_return : RETURN
                        | RETURN expr"""
    p[0] = AST.Return() if len(p) == 1 else AST.Return(p[2])


def p_instruction_print(p):
    """ instruction_print : PRINT printables"""
    p[0] = AST.Print(p[2])


def p_printables(p):
    """ printables : printable
                | printables ',' printable"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_str(p):
    """str : STRING"""
    p[0] = AST.String(p[1])


def p_printable(p):
    """ printable : expr
                | str"""
    p[0] = p[1]


def p_instruction_assign(p):
    """ instruction_assign : assignable '=' expr
                        | assignable ADDASSIGN expr
                        | assignable SUBASSIGN expr
                        | assignable MULASSIGN expr
                        | assignable DIVASSIGN expr"""
    p[0] = AST.AssignOperation(p[2], p[1], p[3])


def p_id(p):
    """id : ID"""
    p[0] = AST.ID(p[1])


def p_assignable(p):
    """ assignable : id
                    | matrix_element
                    | vector_element"""
    p[0] = AST.Assignable(p[1])


def p_matrix_element(p):
    """ matrix_element : id "[" INTNUM "," INTNUM "]" """
    p[0] = AST.Assignable(p[1], (p[3], p[5]))


def p_vector_element(p):
    """ vector_element : id "[" INTNUM "]" """
    p[0] = AST.Assignable(p[1], p[3])


def p_expr(p):
    """expr : expr '\\''"""
    p[0] = AST.Transpose(p[1])


def p_expr_nested(p):
    """expr : '(' expr ')'"""
    p[0] = p[2]


def p_expr_matrix_fun(p):
    """expr : matrix_function '(' expr ')'"""
    p[0] = AST.Function(p[1], p[3])


def p_expr_literal(p):
    """expr : assignable
            | matrix"""
    p[0] = p[1]


def p_expr_minus(p):
    """expr : "-" expr %prec UMINUS"""
    p[0] = AST.Uminus(p[2])


def p_expr_int(p):
    """expr : INTNUM"""
    p[0] = AST.IntNum(p[1])


def p_expr_float(p):
    """expr : FLOAT"""
    p[0] = AST.Float(p[1])


def p_binary_expression(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr DOTADD expr
            | expr DOTSUB expr
            | expr DOTMUL expr
            | expr DOTDIV expr
            | expr '>' expr
            | expr '<' expr
            | expr EQ expr
            | expr NEQ expr
            | expr LEQ expr
            | expr GEQ expr
    """
    p[0] = AST.BinaryExpr(p[1], p[2], p[3])


def p_matrix_function(p):
    """ matrix_function : ZEROS
                            | ONES
                            | EYE"""
    p[0] = p[1]


def p_instruction_if(p):
    """ instruction_if : IF '(' expr ')' instruction %prec IFX
                    | IF '(' expr ')' instruction ELSE instruction"""
    p[0] = AST.IfCondition(p[3], p[5], p[7] if len(p) > 7 else None)


def p_instruction_for(p):
    """ instruction_for : FOR id '=' expr ':' expr instruction"""
    p[0] = AST.For(p[2], p[4], p[6], p[7])


def p_instruction_while(p):
    """ instruction_while : WHILE '(' expr ')' instruction"""
    p[0] = AST.While(p[3], p[5])


# def p_range(p):
#     """range : expr ':' expr """


def p_matrix(p):
    """ matrix : '[' vectors ']'"""
    p[0] = AST.Matrix(p[2])


def p_vectors(p):
    """vectors : vectors ',' vector
               | vector """
    p[0] = p[1] + [p[3]] if len(p) > 3 else [p[1]]


def p_vector(p):
    """vector : '[' variables ']' """
    p[0] = p[2]


def p_variables(p):
    """variables : variables ',' variable
                 | variable """
    p[0] = p[1] + [p[3]] if len(p) > 3 else [p[1]]


def p_variable(p):
    """variable : INTNUM
                | FLOAT
                | assignable """
    p[0] = p[1]


parser = yacc.yacc()