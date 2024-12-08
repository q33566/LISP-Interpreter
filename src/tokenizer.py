import ply.lex as lex
import re
from enum import Enum
from pathlib import Path
from ply.lex import TOKEN

class Token(Enum):
    NUMBER = r'0|[1-9][0-9]*|-[1-9][0-9]*'
    ID = r'[a-z]([a-z]|[0-9]|-)*'
    BOOL_VAL = r'\#t|\#f'
    SEPRATOR = r'\t|\n|\r|\s'

class Reserved(Enum):
    MODULUS = 'mod'
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    DEFINE = 'define'
    FUN = 'fun'
    IF = 'if'

reserved_dict = {word.value: word.name for word in Reserved}
tokens = ([token.name for token in Token] 
          + [reserved.name for reserved in Reserved])
literals = ['+', '-', '*', '/', '>', '<', '=', '(', ')']

@TOKEN(Token.NUMBER.value)
def t_NUMBER(t):
    t.type = Token.NUMBER.name
    return t

@TOKEN(Token.BOOL_VAL.value)
def t_BOOL_VAL(t):
    t.type = Token.BOOL_VAL.name
    return t

@TOKEN(Token.ID.value)
def t_ID(t):
    t.type = reserved_dict.get(t.value, 'ID')
    return t

@TOKEN(Token.SEPRATOR.value)
def t_SEPRATOR(t):
    pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])

    
if __name__ == "__main__":
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