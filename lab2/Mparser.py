from lab3 import scanner
import ply.yacc as yacc

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


def p_instructions(p):
    """ instructions : instruction
                    | instructions instruction"""


def p_instruction(p):
    """ instruction : instruction_if
                | instruction_for
                | instruction_while
                | instruction_return ';'
                | instruction_assign ';'
                | instruction_print ';'
                | BREAK ';'
                | CONTINUE ';'
                | '{' instructions '}'"""


def p_instruction_return(p):
    """ instruction_return : RETURN
                        | RETURN expr"""


def p_instruction_print(p):
    """ instruction_print : PRINT printables"""


def p_printables(p):
    """ printables : printable
                | printables ',' printable"""


def p_printable(p):
    """ printable : expr
                | STRING"""


def p_instruction_assign(p):
    """ instruction_assign : assignable '=' expr
                        | assignable ADDASSIGN expr
                        | assignable SUBASSIGN expr
                        | assignable MULASSIGN expr
                        | assignable DIVASSIGN expr"""


def p_assignable(p):
    """ assignable : ID
                    | matrix_element
                    | vector_element"""


def p_matrix_element(p):
    """ matrix_element : ID "[" INTNUM "," INTNUM "]" """


def p_vector_element(p):
    """ vector_element : ID "[" INTNUM "]" """


def p_expr(p):
    """expr : assignable
            | INTNUM
            | FLOAT
            | matrix
            | matrix_function "(" expr ")"
            | "-" expr %prec UMINUS
            | expr "\'"
            | "(" expr ")"
            | expr '+' expr
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


def p_matrix_function(p):
    """ matrix_function : ZEROS
                            | ONES
                            | EYE"""


def p_instruction_if(p):
    """ instruction_if : IF '(' expr ')' instruction %prec IFX
                    | IF '(' expr ')' instruction ELSE instruction"""


def p_instruction_for(p):
    """ instruction_for : FOR ID '=' range instruction"""


def p_instruction_while(p):
    """ instruction_while : WHILE '(' expr ')' instruction"""


def p_range(p):
    """range : expr ':' expr """


def p_matrix(p):
    """ matrix : '[' vectors ']'"""


def p_vectors(p):
    """vectors : vectors ',' vector
               | vector """


def p_vector(p):
    """vector : '[' variables ']' """


def p_variables(p):
    """variables : variables ',' variable
                 | variable """


def p_variable(p):
    """variable : INTNUM
                | FLOAT
                | assignable """


parser = yacc.yacc()