import ply.lex as lex

# Reserved keywords
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'return': 'RETURN',
    'main': 'MAIN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'void': 'VOID',
    'double': 'DOUBLE',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE'
}

# Token list
tokens = [
    'ID', 'NUMBER', 'CHARACTER', 'STRING',

    # Arithmetic Operators
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
    'INCR', 'DECR',

    # Assignment and Comparison
    'EQUALS', 'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE',

    # Symbols
    'SEMI', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET', 'COLON', 'SCOPE',

] + list(reserved.values())

# Regular expressions for simple tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_MOD        = r'%'
t_INCR       = r'\+\+'
t_DECR       = r'--'

t_EQUALS     = r'='
t_EQ         = r'=='
t_NEQ        = r'!='
t_GT         = r'>'
t_LT         = r'<'
t_GTE        = r'>='
t_LTE        = r'<='

t_SEMI       = r';'
t_COMMA      = r','
t_COLON      = r':'
t_SCOPE      = r'::'

t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'

def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]  # Strip quotes
    return t

def t_CHARACTER(t):
    r"\'([^\\']|\\.)\'"
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?([eE][-+]?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value.lower() else int(t.value)
    return t

# Comments
def t_LINE_COMMENT(t):
    r'//.*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Line tracking
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Lexical error handler
def t_error(t):
    print(f"Lexical Error: Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Build lexer
lexer = lex.lex()