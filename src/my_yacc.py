import ply.yacc as yacc
import ply.lex as lex
from my_lex import tokens
import my_lex
symbol_table = {}
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
    print_stmt : '(' PRINT_NUM exp ')' 
                  | '(' PRINT_BOOL exp ')'
    '''
    if(p.slice[2].type == 'PRINT_NUM'):
        print(int(p[3]))
    else:
        bool_val = '#t' if p[3] else '#f'
        print(bool_val)
        

def p_exps(p):
    '''
    exps : exp exps
         | exp
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
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
    p[0] = p[1]
    
def p_plus(p):
    '''
    plus       : '(' '+' exp exps ')'
    '''
    p[0] = int(p[3] + sum(p[4]))

def p_minus(p):
    '''
    minus      : '(' '-' exp exp ')'
    '''
    p[0] = int(p[3] - p[4])
    
def p_multiply(p):
    '''
    multiply   : '(' '*' exp exps ')'
    '''
    result = p[3]
    for i in p[4]:
        result = result * i
    p[0] = int(result)
    
def p_devide(p):
    '''
    divide     : '(' '/' exp exp ')'
    '''
    p[0] = int(p[3] / p[4])

def p_modulus(p):
    '''
    modulus    : '(' MODULUS exp exp ')'
    '''
    p[0] = p[3] % p[4]
    
def p_greater(p):
    '''
    greater    : '(' '>' exp exp ')'
    '''
    p[0] = p[3] > p[4]

def p_smaller(p):
    '''
    smaller    : '(' '<' exp exp ')'
    '''
    p[0] = p[3] < p[4]
    
def p_equal(p):
    '''
    equal      : '(' '=' exp exps ')' 
    '''
    def check_same_element(my_list):
        tmp = my_list[0]
        for i in my_list:
            if i!=tmp:
                return False
        return True
    my_list = [p[3]] + p[4]
    p[0] = check_same_element(my_list)
    
def p_ligical_op(p):
    '''
    logical_op : and_op
                 | or_op
                 | not_op
    '''
    p[0] = p[1]
    
def p_and_op(p):
    '''
    and_op    : '(' AND exp exps ')'
    '''
    def and_list(my_list):
        return not (False in my_list)
    my_list = p[4]+[p[3]]
    p[0] = and_list(my_list)
    
def p_or_op(p):
    '''
    or_op     : '(' OR exp exps ')'
    '''
    def or_list(my_list):
        return True in my_list
    # The following is wrong because p[4] may be only one element, not a list.
    # my_list = p[4].append(p[3])
    my_list = [p[3]] + p[4]
    p[0] = or_list(my_list)
    
    
def p_not_op(p):
    '''
    not_op    : '(' NOT exp ')'
    '''
    p[0] = not p[3]
    
def p_def_stmt(p):
    '''
    def_stmt : '(' DEFINE ID exp ')'
    '''
    variable_name = p[3]
    symbol_table[variable_name] = p[4]
    
def p_fun_exp(p):
    '''
    fun_exp : '(' FUN fun_ids exp ')'
    '''
    def fun(*args):
        param_names = p[3]
        func_body = p[4]
        local_scope = {name: value for name, value in zip(param_names, args)}
        return eval_fun_body(body=func_body, local_scope=local_scope)
    p[0] = fun
    pass

def p_fun_ids(p):
    '''
    fun_ids : '(' ids ')'
    '''
    p[0] = p[1]
    
def p_ids(p):
    '''
    ids : ID ids
       | empty
    '''
    if(len(p)==3):
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_last_exp(p):
    #不知道會不會用到
    '''
    last_exp : exp
    '''
    pass
def p_fun_call(p):
    '''
    fun_call : fun_exp params
            | fun_name params
    '''
    fun = p[1]
    params = p[2]
    print(params)
    p[0] = fun(*params)

def p_params(p):
    '''
    params : param params
          | empty
    '''
    if len(p) == 3:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []
def p_param(p):
    '''
    param : exp
    '''
    p[0] = p[1]

def p_variable(p):
    '''
    variable : ID
    '''
    variable_name = p[1]
    if variable_name in symbol_table:
        p[0] = symbol_table[variable_name]
    else:
        raise NameError(f"Variable '{variable_name}' is not defined")
    
def p_fun_name(p):
    '''
    fun_name : ID
    '''
    p[0] = p[1]
def p_if_exp(p):
    '''
    if_exp : '(' IF exp exp exp ')'
    '''
    if p[3]:
        p[0] = p[4]
    else:
        p[0] = p[5]
    
    
# Error rule for syntax errors
def p_error(p):
    raise SyntaxError("syntax error")

def build_parser():
    return yacc.yacc(debug=False)

def parse_input(s, parser=None):
    if parser is None:
        parser = build_parser()
    lexer = lex.lex(module=my_lex)
    try:
        parse_result = parser.parse(s, lexer=lexer)
        return parse_result
    except SyntaxError:
        print('syntax error')
        return 'syntax error'

def eval_fun_body(body, local_scope):
    global symbol_table
    original_scope_table = symbol_table.copy()
    symbol_table.update(local_scope)
    try:
        return parse_input(body)
    finally:
        symbol_table = original_scope_table

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
        lexer = lex.lex(module=my_lex)
        try:
            result = parser.parse(s, lexer = lexer)
        except SyntaxError:
            print('syntax error')
            pass