from lexer import lexer
from parser import parser, reset_symbol_table

def run_code(code_string):
    errors = []

    # ---------- Lexical Analysis ----------
    lexer.lineno = 1
    lexer.input(code_string)
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Optional: Uncomment to debug tokens
        # print(f"{tok.type}('{tok.value}') at line {tok.lineno}")

    # ---------- Syntax & Semantic Analysis ----------
    reset_symbol_table()

    # Capture error outputs
    import builtins
    original_print = print
    error_lines = []

    def capture_print(*args, **kwargs):
        error_lines.append(" ".join(str(arg) for arg in args))

    builtins.print = capture_print

    try:
        parser.parse(code_string, lexer=lexer)
    except Exception as e:
        error_lines.append(f"Unexpected Error: {e}")
    finally:
        builtins.print = original_print

    errors.extend(error_lines)
    return errors

# ---------- Run from test_code.txt ----------
if __name__ == "__main__":
    import sys
    import os

    filename = "test_code.txt"
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        sys.exit(1)

    with open(filename, "r") as file:
        code = file.read()

    errors = run_code(code)

    if errors:
        print("Errors found:")
        for err in errors:
            print(f"  -> {err}")
    else:
        print("No errors found.")