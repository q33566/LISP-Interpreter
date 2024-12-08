import ply.lex as lex
import re
from enum import Enum

separator = r'\t|\n|\r|\s'
letter = '[a-z]'
digit = '[0-9]'

class Token(Enum):
    NUMBER = r'0|[1-9][0-9]*|-[1-9][0-9]*'
    ID = r'[a-z]([a-z]|[0-9]|-)*'
    BOOL_VAL = r'\#t|\#f'
    LEFT_PARENTHESES = r'\('
    RIGHT_PARENTHESES = r'\)'
    SEPRATOR = separator

class Operator(Enum):
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    GREATER = '>'
    SMALLER = '<'
    EQUAL = '='

class Reserved(Enum):
    MODULUS = 'mod'
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    DEFINE = 'define'
    FUN = 'fun'
    IF = 'if'

reserved_dict = {word.value: word.name for word in Reserved}
operator_dict = {word.value: word.name for word in Operator}
tokens = ([token.name for token in Token] 
          + [reserved.name for reserved in Reserved] 
          + [operator.name for operator in Operator])

def t_NUMBER(t):
    t.type = Token.NUMBER.name
    return t
def t_BOOL_VAL(t):
    t.type = Token.BOOL_VAL.name
    return t
def t_ID(t):
    t.type = reserved_dict.get(t.value, 'ID')
    return t
def t_OPERATOR(t):
    t.type = operator_dict.get(t.value)
    return t
def t_LEFT_PARENTHESES(t):
    t.type = Token.LEFT_PARENTHESES.name
    return t
def t_RIGHT_PARENTHESES(t):
    t.type = Token.RIGHT_PARENTHESES.name
    return t
def t_SEPRATOR(t):
    pass
def t_error(t):
    print("Illegal character '%s'" % t.value[0])

def set_up_regex_pattern():
    t_NUMBER.__doc__ = Token.NUMBER.value
    t_BOOL_VAL.__doc__ = Token.BOOL_VAL.value
    t_ID.__doc__ = Token.ID.value
    t_OPERATOR.__doc__ = '|'.join(re.escape(op.value) for op in Operator)
    t_SEPRATOR.__doc__ = Token.SEPRATOR.value
    t_LEFT_PARENTHESES.__doc__ = Token.LEFT_PARENTHESES.value
    t_RIGHT_PARENTHESES.__doc__ = Token.RIGHT_PARENTHESES.value
    
if __name__ == "__main__":
    set_up_regex_pattern()
    lexer = lex.lex()
    # test_data_path = Path('../public_test_data')
    # for file in test_data_path.iterdir():
    #     content = file.read_text(encoding='utf-8')
    #     print(content)
    #     # Give the lexer some input
    #     lexer.input(content)
    #     # Tokenize
    #     while True:
    #         tok = lexer.token()
    #         if not tok:
    #             break      # No more input
    #         print(tok)
    #     print('finish')
    # lexer.input("""
    # (define foo)
    # """)
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break      # No more input
    #     print(tok)
    # print('finish')