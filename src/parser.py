import ply.yacc as yacc
import ply.lex as lex
from tokenizer import tokens
import tokenizer

start = 'program'   
def p_empty(p):
    'empty :'
    pass

def p_program(p):
    '''
    program : stmts
    '''
    
def p_stmts(p):
    '''
    stmts : stmt stmts
             | stmt 
    '''
def p_stmt(p):
    '''
    stmt : exp
            | def_stmt
            | print_stmt
    '''
    if(p[1] == 'def'):
        pass
    elif(p[1] == 'print'):
        pass
    else:
        p[0] = p[1]
def p_print_stmt(p):
    '''
    print_stmt : '(' PRINT_NUM ')' exp
                  | '(' PRINT_BOOL ')' exp
    '''             
def p_exps(p):
    '''
    exps : exp exps
         | exp
    '''
    if(len(p) == 3):
        p[0] = p[2].append(p[1])
    else:
        p[0] = [p[1]]
    
def p_exp(p):
    '''
    exp : BOOL_VAL
        | NUMBER
        | variable
        | num_op
        | logical_op
        | fun_exp
        | fun_call
        | if_exp
    '''
    print('exp')
    p[0] = p[1]

def p_num_op(p):
    '''
    num_op  : plus
            | minus
            | multiply
            | divide
            | modulus
            | greater
            | smaller
            | equal
    '''
    print('num_op')
    p[0] = p[1]
    
def p_plus(p):
    '''
    plus       : '(' '+' exp exps ')'
    '''
    p[0] = p[3] + sum(p[4])
    print('plus')
    

def p_minus(p):
    '''
    minus      : '(' '-' exp exp ')'
    '''
    print('minus')
    p[0] = p[3] - p[4]
    
def p_multiply(p):
    '''
    multiply   : '(' '*' exp exp exps ')'
    '''
    print('multiply')
    def multiply_list(my_list):
        tmp = 1
        for i in my_list:
            tmp = tmp * i
        return tmp
    my_list = p[4].append(p[3])
    p[0] = multiply_list(my_list)
    
def p_devide(p):
    '''
    divide     : '(' '/' exp exp ')'
    '''
    print('divide')
    p[0] = p[3] / p[4]

def p_modulus(p):
    '''
    modulus    : '(' MODULUS exp exp ')'
    '''
    print('modulus')
    p[0] = p[3] % p[4]
    
def p_greater(p):
    '''
    greater    : '(' '>' exp exp ')'
    '''
    print('greater')
    p[0] = p[3] > p[4]

def p_smaller(p):
    '''
    smaller    : '(' '<' exp exp ')'
    '''
    print('smaller')
    p[0] = p[3] < p[4]
    
def p_equal(p):
    '''
    equal      : '(' '=' exp exps ')' 
    '''
    print('equal')
    def check_same_element(my_list):
        tmp = my_list[0]
        for i in my_list:
            if i!=tmp:
                return False
        return True
    my_list = p[4].append(p[3])
    p[0] = check_same_element(my_list)
    
def p_ligical_op(p):
    '''
    logical_op : and_op
                 | or_op
                 | not_op
    '''
    print('logical_op')
    
def p_and_op(p):
    '''
    and_op    : '(' AND exp exps ')'
    '''
    def and_list(my_list):
        return not False in my_list
    my_list = p[4].append(p[3])
    p[0] = and_list(my_list)
    print('and_op')
    
def p_or_op(p):
    '''
    or_op     : '(' OR exp exps ')'
    '''
    def or_list(my_list):
        return not True in my_list
    my_list = p[4].append(p[3])
    p[0] = or_list(my_list)
    print('or_op')
    
    
def p_not_op(p):
    '''
    not_op    : '(' NOT exp ')'
    '''
    p[0] = not p[3]
    print('not_op')
    
def p_def_stmt(p):
    '''
    def_stmt : '(' DEFINE variable exp ')'
    '''
    p[3] = p[4] 
    print('def_stmt')
    
def p_variable(p):
    '''
    variable : ID
    '''
    p[0] = p[1]
    print('variable')
    
def p_fun_exp(p):
    '''
    fun_exp : '(' FUN fun_ids fun_body ')'
    fun_ids : '(' ids ')'
    ids : ID ids
       | empty
    fun_body : exp
    params : param params
          | empty
    fun_call : fun_exp params
            | fun_name params
    param : exp
    last_exp : exp
    fun_name : ID
    '''
def p_if_exp(p):
    '''
    if_exp : '(' IF test_exp then_exp else_exp ')'
    test_exp : exp
    then_exp : exp
    else_exp : exp
    '''
    
# Error rule for syntax errors
def p_error(p):
    print("syntax error")
    return('syntax error')

def build_parser():
    return yacc.yacc(debug=False)

def parse_input(s, parser=None):
    if parser is None:
        parser = build_parser()
    lexer = lex.lex(module=tokenizer)
    return parser.parse(s, lexer=lexer)

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)
if __name__ == "__main__":
    # Build the parser
    parser = yacc.yacc(debug=True)
    while True:
        try:
            s = input('input: ')
        except EOFError:
            break
        if not s: continue
        lexer = lex.lex(module=tokenizer)
        result = parser.parse(s, lexer = lexer)
        print(result)