import ply.yacc as yacc
from lexer import tokens

# Symbol table: { var_name: {'type': ..., 'line': ...} }
symbol_table = {}

# Utility: error reporting
def report_error(message, lineno=None):
    location = f" on line {lineno}" if lineno else ""
    print(f"Error{location}: {message}")

# --------- Grammar Rules ---------

def p_program(p):
    'program : INT MAIN LPAREN RPAREN LBRACE statements RETURN NUMBER SEMI RBRACE'
    if p[8] != 0:
        report_error("Semantic Warning: return value is not 0", lineno=p.lineno(8))

def p_statements(p):
    '''statements : statement statements
                  | statement'''
    pass

# Declarations
def p_statement_decl(p):
    '''statement : INT ID SEMI
                 | FLOAT ID SEMI
                 | CHAR ID SEMI'''
    dtype, var = p[1], p[2]
    var_line = p.slice[2].lineno
    if var in symbol_table:
        prev_line = symbol_table[var]['line']
        report_error(f"Variable '{var}' already declared (originally at line {prev_line})", var_line)
    else:
        symbol_table[var] = {'type': dtype, 'line': var_line}


# Assignments
def p_statement_assign(p):
    'statement : ID EQUALS expression SEMI'
    var = p[1]
    var_line = p.slice[1].lineno
    if var not in symbol_table:
        report_error(f"Variable '{var}' not declared before use", var_line)

# Expressions
def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    pass

def p_expression_term(p):
    'expression : term'

def p_term(p):
    '''term : ID
            | NUMBER
            | CHARACTER'''
    if isinstance(p[1], str) and p.slice[1].type == 'ID':
        var = p[1]
        var_line = p.slice[1].lineno
        if var not in symbol_table:
            report_error(f"Use of undeclared variable '{var}'", var_line)

# Syntax Error Handler
def p_error(p):
    if p:
        report_error(f"Syntax Error: Unexpected token '{p.value}'", p.lineno)
    else:
        print("Syntax Error: Unexpected end of input")

# --------- Build Parser ---------
parser = yacc.yacc()

# --------- Reset Function ---------
def reset_symbol_table():
    global symbol_table
    symbol_table = {}