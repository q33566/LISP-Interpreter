import ply.yacc as yacc
import ply.lex as lex
from utils.my_eval import *
from my_lex import tokens
from utils.my_ast import *
import my_lex
visitor = Visitor()
#evaluator = Evaluator()
# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()
start = 'program'
def p_empty(p):
    'empty : '
    p[0] = None

def p_program(p):
    '''
    program : stmts
    '''
    p[0] = Program(stmts=p[1])
    
def p_stmts(p):
    '''
    stmts : stmt stmts
             | stmt 
    '''

    if len(p) == 3:
        if p[1] != None:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = p[2]
    else:
        if p[1] is not None:
            p[0] = [p[1]]
        else:
            p[0] = []
        
def p_stmt(p):
    '''
    stmt : exp
            | def_stmt
            | print_stmt
    '''
    p[0] = p[1]
    
def p_print_stmt(p):
    '''
    print_stmt : '(' PRINT_NUM exp ')' 
                  | '(' PRINT_BOOL exp ')'
    '''
    print_type = p.slice[2].type
    exp = p[3]
    p[0] = Print(exp=exp, print_type=print_type)
        

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
    operator = '+'
    operands = [p[3]] + p[4]
    p[0] = NumOp(operator=operator, operands=operands)

def p_minus(p):
    '''
    minus      : '(' '-' exp exp ')'
    '''
    operator = '-'
    operands = [p[3], p[4]]
    p[0] = NumOp(operator=operator, operands=operands)
    
def p_multiply(p):
    '''
    multiply   : '(' '*' exp exps ')'
    '''
    operator = '*'
    operands = [p[3]] + p[4]
    p[0] = NumOp(operator=operator, operands=operands)
    
def p_divide(p):
    '''
    divide     : '(' '/' exp exp ')'
    '''
    operator = '/'
    operands = [p[3], p[4]]
    p[0] = NumOp(operator=operator, operands=operands)

def p_modulus(p):
    '''
    modulus    : '(' MODULUS exp exp ')'
    '''
    operator = '%'
    operands = [p[3], p[4]]
    p[0] = NumOp(operator=operator, operands=operands)
    
def p_greater(p):
    '''
    greater    : '(' '>' exp exp ')'
    '''
    operator = '>'
    operands = [p[3], p[4]]
    p[0] = NumOp(operator=operator, operands=operands)

def p_smaller(p):
    '''
    smaller    : '(' '<' exp exp ')'
    '''
    operator = '<'
    operands = [p[3], p[4]]
    p[0] = NumOp(operator=operator, operands=operands)
    
def p_equal(p):
    '''
    equal      : '(' '=' exp exps ')' 
    '''
    operator = '='
    operands = [p[3]] + p[4]
    p[0] = NumOp(operator=operator, operands=operands)
    
def p_logical_op(p):
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
    operator = 'and'
    operands = [p[3]] + p[4]
    p[0] = LogicalOp(operator=operator, operands=operands)
    
def p_or_op(p):
    '''
    or_op     : '(' OR exp exps ')'
    '''
    operator = 'or'
    operands = [p[3]] + p[4]
    p[0] = LogicalOp(operator=operator, operands=operands)
    
def p_not_op(p):
    '''
    not_op    : '(' NOT exp ')'
    '''
    operator = 'not'
    operands = [p[3]]
    p[0] = LogicalOp(operator=operator, operands=operands)
    
def p_def_stmt(p):
    '''
    def_stmt : '(' DEFINE variable exp ')'
    '''
    variable_node = p[3]
    value = p[4]
    p[0] = AstNode(node_type=NodeType.DEFINE, children=[variable_node, value], leaf='define')

def p_def_stmts(p):
    '''
    def_stmts : empty
              | def_stmts def_stmt
    '''
    if len(p) == 3:
        if p[1] is not None:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[2]]
    else:
        if p[1] is not None:
            p[0] = [p[1]]
        else:
            p[0] = []
            
def p_fun_exp(p):
    '''
    fun_exp : '(' FUN fun_ids fun_body ')'
    '''
    fun_ids: list = p[3]
    func_body = p[4]
    #fun_ids_node = AstNode(node_type=NodeType.FUN_IDS, leaf=fun_ids)
    #p[0] = AstNode(node_type=NodeType.FUN, children=[fun_ids_node, func_body], leaf='fun')
    p[0] = AstNode(node_type=NodeType.FUN, children=[fun_ids, func_body], leaf='fun')
    
def p_fun_body(p):
    '''
    fun_body : def_stmts exp
    '''
    if len(p) == 3:
        # 將 def_stmts 和 exp 結合起來作為函數體
        p[0] = AstNode(node_type=NodeType.FUN_BODY, children=p[1] + [p[2]], leaf=None)
    else:
        # 只有一個表達式
        p[0] = p[1]
    
def p_fun_ids(p):
    '''
    fun_ids : '(' ids ')'
    '''
    p[0] = p[2]
    
def p_ids(p):
    '''
    ids : ID ids
       | empty
    '''
    if(len(p)==3):
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# def p_last_exp(p):
#     #不知道會不會用到
#     '''
#     last_exp : exp
#     '''
    
def p_fun_call(p):
    '''
    fun_call : '(' fun_exp params ')'
            | '(' fun_name params ')'
    '''
    fun_node = p[2]
    params = p[3]
    p[0] = AstNode(node_type=NodeType.FUN_CALL, children=[fun_node] + params, leaf='fun_call')

def p_params(p):
    '''
    params : param params
          | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
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
    var_name = p[1]
    p[0] = AstNode(node_type=NodeType.VARIABLE, leaf=var_name)

    
def p_fun_name(p):
    '''
    fun_name : ID
    '''
    fun_name = p[1]
    p[0] = AstNode(node_type=NodeType.VARIABLE, children=[], leaf=fun_name)
    
def p_if_exp(p):
    '''
    if_exp : '(' IF exp exp exp ')'
    '''
    condition = p[3]
    true_branch = p[4]
    false_branch = p[5]
    p[0] = IfExp(condition=condition, true_branch=true_branch, false_branch=false_branch)
    
def p_error(p):
    raise SyntaxError("syntax error")



def parse_input(s):
    parser = yacc.yacc(debug=True, debuglog=log)

    lexer = lex.lex(module=my_lex)
    try:
        result = parser.parse(s, lexer=lexer, debug=log)

        if isinstance(result, AstNode):
            result.accept(visitor)
        else:
            print('yacc的return 怪怪的')
    # except NameError as e:
    #     print(e)
    # except TypeError as e:
    #     print(e)
    # except ValueError as e:
    #     print(e)
    # except EvalError as e:
    #     if str(e) == "Type error!":
    #         print("Type error!")
    #     else:
    #         print(f"Evaluation error: {e}")
    except SyntaxError as e:
        print('syntax error')

def print_ast(ast, indent=0):
    spacing = '  ' * indent
    if isinstance(ast, AstNode):
        print(f"{spacing}{ast.node_type.name}: {ast.leaf}")
        for child in ast.children:
            print_ast(child, indent + 1)
    elif isinstance(ast, list):
        for item in ast:
            print_ast(item, indent)
    else:
        print(f"{spacing}{ast}")

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)
if __name__ == "__main__":
    # Build the parser
    while True:
        try:
            s = input('input: ')
        except EOFError:
            break
        if not s:
            continue
        parse_input(s)
            