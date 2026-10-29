"""
Syntax and Semantic Verification Gate for RepoGuard.
Ensures code generated or modified by LLM agents is syntactically valid Python
prior to re-audit verification or disk persistence.
"""
import ast
from typing import Tuple, Optional


def validate_python_syntax(code_string: str) -> Tuple[bool, Optional[str]]:
    """
    Parses candidate code using Python's native AST compiler.
    
    Returns:
        Tuple[bool, Optional[str]]: (True, None) if valid Python, 
                                    (False, error_details) if a SyntaxError is encountered.
    """
    try:
        ast.parse(code_string)
        return True, None
    except SyntaxError as e:
        error_msg = f"SyntaxError at line {e.lineno}, offset {e.offset}: {e.msg}"
        if e.text:
            error_msg += f"\n  --> {e.text.strip()}"
        return False, error_msg
    except Exception as e:
        return False, f"Unexpected AST validation error: {str(e)}"
