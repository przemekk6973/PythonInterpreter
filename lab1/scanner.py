import ply.lex as lex

#mapa słów kluczowych, aby rozpoznawanie identyfikatorów i słów kluczowych w jednym skanerze działało poprawnie
reserved = {
    'if': 'IF',
    'for': 'FOR',
    'else': 'ELSE',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT',
}

#leksemy, do których odwołujemy się jednoznakowo
literals = "=+-*/()[]{}<>:,';"

#leksemy
tokens = list(reserved.values()) + [
    'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
    'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
    'LEQ', 'GEQ', 'EQ', 'NEQ',
    'ID', 'INTNUM', 'FLOAT', 'STRING',
]

#ignorowanie znaku nowej linii i komentarza
t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

#wyrażenia regularne do leksemów
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LEQ = r'<='
t_GEQ = r'>='
t_EQ = r'=='
t_NEQ = r'!='
t_INTNUM = r'\d+'
t_FLOAT = r'(\d+\.\d*|\.\d+)([eE][-]?\d+)?'
t_STRING = r'\"(\\.|[^"\\\n])*\"'


#przekazywanie wartości
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

#numerowanie linii, ignorowanie newline
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#gdy nie zna wprowadzonego znaku
def t_error(t):
    print("(%d): illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()