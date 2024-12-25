from enum import Enum
from ply.lex import TOKEN
from utils.my_eval import *

class Token(Enum):
    NUMBER = r'0|[1-9][0-9]*|-[1-9][0-9]*'
    ID = r'[a-z]([a-z]|[0-9]|-)*'
    BOOL_VAL = r'\#t|\#f'
    SEPRATOR = r'\t|\n|\r|\s'
    PRINT_NUM = r'print-num'
    PRINT_BOOL = r'print-bool'

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
    t.value = Number(value=int(t.value))
    return t

@TOKEN(Token.BOOL_VAL.value)
def t_BOOL_VAL(t):
    t.type = Token.BOOL_VAL.name
    t.value = Boolean(value=True) if t.value == '#t' else Boolean(value=False)
    return t

@TOKEN(Token.PRINT_BOOL.value)
def t_PRINT_BOOL(t):
    t.type = Token.PRINT_BOOL.name
    return t

@TOKEN(Token.PRINT_NUM.value)
def t_PRINT_NUM(t):
    t.type = Token.PRINT_NUM.name
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